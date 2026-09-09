import graphene
from graphene_django import DjangoObjectType
from core.permissions import login_required
from .models import Project, Task

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