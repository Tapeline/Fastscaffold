from fastscaffold.std.gen import SimpleTemplateRender


class ArgonSecurityGen(SimpleTemplateRender):
    location = ["infrastructure", "security.py"]
    template = "auth/security_impl.py.template"
