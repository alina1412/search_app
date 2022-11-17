from fastapi import APIRouter, Depends, status


api_router = APIRouter(
    prefix="/v1",
    tags=["private"],
)


@api_router.post(
    "/data",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
        
    },
)
def get_data(
    # user_input: User = Depends(),
    # user_token_data=Depends(get_user_by_token)
):
    """Page can be seen if user registered and
    header has  -H 'Authorization:bearer' and
    -H 'client_secret:<user-token>"""

    return {"data": "user_token_data"}
