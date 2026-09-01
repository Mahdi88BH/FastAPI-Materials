from fastapi import Header, FastAPI, Depends, HTTPException, status, APIRouter




async def secret_header(secret_header: str | None = Header(None)) -> None:
    if not secret_header or secret_header != "SECRET_VALUE":
        raise HTTPException(status.HTTP_403_FORBIDDEN)


# Using a dependency on a whole application
app = FastAPI(dependencies= [Depends(secret_header)])

router = APIRouter(dependencies= [Depends(secret_header)])
app.include_router(router, prefix="/router")


# Using a dependency on a path decorator
@app.get("/protected-route", dependencies= [Depends(secret_header)])
async def protected_route():
    return {"hello": "world"}


# Using a dependency on a whole router
@router.get("/route1")
async def router_route1():
        return {"route": "route1"}

@router.get("/route2")
async def router_route2():
        return {"route": "route2"}