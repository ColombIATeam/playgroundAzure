import uvicorn

if not __name__.startswith("__mp"):
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    from api.common.dependency_container import DependencyContainer
    from api.workflows.health_checks import health_check_router
    from api.workflows import question_router

    DependencyContainer.initialize()
    app = FastAPI(title="PreparadorPlayGround", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_check_router.router)
    app.include_router(question_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)