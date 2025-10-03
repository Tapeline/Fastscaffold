from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.core.execution import ScaffoldExecutor
from fastscaffold.io import save_files
from fastscaffold.std.configs import WebProjectConfig
from fastscaffold.std.gen import AddImports, SourceGen, import_from, src_in
from fastscaffold.std.jinja import create_jinja
from fastscaffold.std.py.algo import ArgonSecurityGen
from fastscaffold.std.py.application.basic_user import (
    BasicAppAuthGen,
    BasicAppAuthInteractorsGen,
)
from fastscaffold.std.py.application.interactors import (
    CreateInteractorGen,
    DeleteInteractorGen,
    ListInteractorGen,
    ReadInteractorGen,
    UpdateInteractorGen,
)
from fastscaffold.std.py.application.persistence import (
    PaginationDTOGen,
    UUIDGeneratorInterfaceGen, UoWInterfaceGen,
)
from fastscaffold.std.py.application.persistence import GatewayInterfaceGen
from fastscaffold.std.py.bootstrap import (
    AlgoDIProviderGen, ConfigDIProviderGen,
    ConfigGen,
    DEFAULT_PG_CONF,
    DEFAULT_SECURITY_CONF,
    LitestarAppGen,
    LitestarAuthProviderGen,
    UoWProviderGen,
)
from fastscaffold.std.py.configs import PyQAConfigsGen, PyprojectGen
from fastscaffold.std.py.domain import EntityGen
from fastscaffold.std.py.infrastructure.persistence import (
    AlembicGen,
    SqlalchemyModelsGen,
    SqlalchemySecurityGen, SqlalchemySessionGen,
    SqlalchemySimpleGatewayImplGen,
    SqlalchemyUoWGen, UUIDGeneratorImplGen,
)
from fastscaffold.std.py.presentation.litestar import (
    LitestarCommonUserEndpointsGen,
    LitestarCommonsGen,
)


def test():
    def scaffold(ctx: ScaffoldRunContext) -> list[ScaffoldComponent]:
        ctx += WebProjectConfig("Note taking app", "notetaker")
        ctx += create_jinja()

        return [
            EntityGen(
                name="User",
                fields=dict(
                    username="str",
                ),
                with_id=True
            ),
            EntityGen(
                name="Note",
                fields=dict(
                    name="str",
                    content="str",
                    author_id="UserId"
                ),
                with_id=True,
                add_imports=[
                    "from notetaker.domain.user import UserId"
                ],
            ),
            UoWInterfaceGen(),
            GatewayInterfaceGen(
                "User",
                GatewayInterfaceGen.add_get_by_id(),
                GatewayInterfaceGen.add_save()
            ),
            PaginationDTOGen(),
            UUIDGeneratorInterfaceGen(),
            GatewayInterfaceGen(
                "Note",
                GatewayInterfaceGen.add_get_by_id(),
                GatewayInterfaceGen.add_save(),
                GatewayInterfaceGen.add_get_paginated_filtered(
                    "get_of_user",
                    author_id="UserId"
                ),
                GatewayInterfaceGen.add_delete_by_id(),
                gen_exceptions=True
            ),
            AddImports(
                src_in("application", "persistence", "note.py"),
                "from notetaker.domain.user import UserId"
            ),
            BasicAppAuthGen("User"),
            BasicAppAuthInteractorsGen("User"),
            CreateInteractorGen("Note"),
            ReadInteractorGen("Note", with_auth=False),
            UpdateInteractorGen("Note"),
            DeleteInteractorGen("Note"),
            ListInteractorGen(
                "Note", with_auth=False, gw_list_method="get_of_user"
            ),
            AlembicGen(),
            SqlalchemyUoWGen(),
            SqlalchemyModelsGen(["User", "Note"]),
            SqlalchemySimpleGatewayImplGen(
                "User",
                get_by_id=True, save=True
            ),
            AddImports(
                src_in("infrastructure", "persistence", "user.py"),
                "from notetaker.application.auth.exceptions import UserNotFound"
            ),
            SqlalchemySimpleGatewayImplGen(
                "Note",
                get_by_id=True, save=True
            ),
            SqlalchemySecurityGen(),
            UUIDGeneratorImplGen(),
            ArgonSecurityGen(),
            LitestarCommonsGen(),
            LitestarCommonUserEndpointsGen(),
            SqlalchemySessionGen(),
            ConfigGen(
                DEFAULT_PG_CONF,
                DEFAULT_SECURITY_CONF,
            ),
            ConfigDIProviderGen(),
            AlgoDIProviderGen(),
            LitestarAuthProviderGen(),
            UoWProviderGen(),
            LitestarAppGen(),
            PyprojectGen(),
            PyQAConfigsGen(),
        ]

    executor = ScaffoldExecutor()
    files = executor.run(scaffold)
    #save_files("../../GeneratedNoteTakingApp", files)
    save_files("generated_1", files)


if __name__ == "__main__":
    test()
