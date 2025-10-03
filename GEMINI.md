Fastscaffold is a project that aims to minimize boilerplate that is needed to
write each time you start a Clean Architecture service in Python.

The main idea is that your template consists of different prebuilt components that
you can combine, opt-in and opt-out based on whether you want them in your project or not.
 
Components can access (read and modify) **context**. Context is a collection of
different objects that describe what's happening in the project. Templates will be
adjusted based on what's in context. E.g. if you define a `User(username: str, age: int)`
entity, and then generate a `User` SQLAlchemy model, it will actually contain  
`username: str, age: int`, because `User` entity definition was saved to context by
entity component and then read by SQLAlchemy model component.
