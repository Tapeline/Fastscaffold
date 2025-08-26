from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.core.execution import ScaffoldExecutor
from fastscaffold.io import save_files
from fastscaffold.std.configs import ArchitectureConfig, WebProjectConfig
from fastscaffold.std.gen import AddImports, SourceGen, import_from, src_in
from fastscaffold.std.jinja import create_jinja
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
    UoWInterfaceGen,
)
from fastscaffold.std.py.application.persistence import GatewayInterfaceGen
from fastscaffold.std.py.domain import EntityGen
from fastscaffold.std.py.infrastructure.persistence import (
    AlembicGen,
    SqlalchemyModelsGen,
)


def test():
    def scaffold(ctx: ScaffoldRunContext) -> list[ScaffoldComponent]:
        ctx += WebProjectConfig("Test Project", "test_proj")
        ctx += ArchitectureConfig()
        ctx += create_jinja()

        return [
            EntityGen(
                name="User",
                fields=dict(
                    username="str",
                    hashed_password="str",
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
                    "from test_proj.domain.user import UserId"
                ],
            ),
            UoWInterfaceGen(),
            GatewayInterfaceGen(
                "User",
                GatewayInterfaceGen.add_get_by_id,
                GatewayInterfaceGen.add_save
            ),
            PaginationDTOGen(),
            GatewayInterfaceGen(
                "Note",
                GatewayInterfaceGen.add_get_by_id,
                GatewayInterfaceGen.add_save,
                GatewayInterfaceGen.add_get_paginated_filtered(
                    "get_of_user",
                    author_id="UserId"
                )
            ),
            AddImports(
                src_in("application", "persistence", "note.py"),
                "from test_proj.domain.user import UserId"
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
            SqlalchemyModelsGen(["User", "Note"]),
        ]

    executor = ScaffoldExecutor()
    files = executor.run(scaffold)
    save_files("test_result", files)


if __name__ == "__main__":
    test()
