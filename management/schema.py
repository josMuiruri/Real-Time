import graphene
from graphene_django import DjangoObjectType
from core.permissions import login_required
from .models import Project, Task
from channels.layers import get_channel_layer


class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ('id', 'project', 'title', 'status', 'assigned_to')

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'created_at', 'owner', 'tasks')

class Query(graphene.ObjectType):
    my_projects = graphene.List(ProjectType)

    @login_required
    def resolve_my_projects(self, info):
        # optimization: (prefetch_related) -> stops N+1 query loops on db
        return Project.objects.filter(owner=info.context.user).prefetch_related('tasks')

class CreateProject(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    project = graphene.Field(ProjectType)

    @login_required
    def mutate(self, info, name, description=''):
        project = Project(name=name, description=description, owner=info.context.user)
        project.save()
        return CreateProject(project=project)

class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()

class Subscription(graphene.ObjectType):
    task_updated = graphene.Field(TaskType, project_id=graphene.Int(required=True))

    @login_required
    def resolve_task_updated(root, info, project_id):
        from .model import Project
        if not Project.objects.filter(id=project_id, owner=info.context.user).exists():
            raise Exception('Unauthorized access to this project stream.')

        channel_layer = get_channel_layer()
        group_name = f'project_{project_id}'

        async def event_stream():
            # dynamically allocate an isolated connection queue path for this socket
            channel_name = await channel_layer.new_channel()
            await channel_layer.group_add(group_name, channel_name)

            try:
                while True:
                    # listen continuously for messages routed via redis channel layer
                    message = await channel_layer.receive(channel_name)
                    if message['type'] == 'task_update_event':
                        yield {'task_updated': Task.objects.get(pk=message['task_id'])}
            finally:
                # clean up & discard the channel if user closes their browser tab
                await channel_layer.group_discard(group_name, channel_name)

        return event_stream()