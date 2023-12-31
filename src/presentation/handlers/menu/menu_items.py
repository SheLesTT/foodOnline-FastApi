from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from starlette import status

from src.presentation.handlers.responces.exceptions.main import MenuItemNotFound
from src.domain.menu.dto.all_schemas import BaseMenuItem
from src.domain.menu.exceptions.menu_item import MenuItemNotExists
from src.domain.menu.usecases.menu_item_service import MenuItemService
from src.presentation.api.di.providers.services import  get_menu_item_service

router = APIRouter(
    prefix='/menuitems',
    tags=["Posts"]
)

query_params = {"name": (str, "carbonara")}

@router.get("/",
            description="Get all menu items")
async def get_menu_items(
        item_service: Annotated[MenuItemService, Depends(get_menu_item_service)],
        request: Request
        )-> list[BaseMenuItem] | None:

    menu_items = await item_service.get_all_items(request.query_params)
    return menu_items

@router.get(
    "/{id}",
    responses= {status.HTTP_404_NOT_FOUND: {"model": MenuItemNotFound}},
    description="Get menu item by ID"
)
async def get_menu_item(
        id: str,response: Response,
        item_service: Annotated[MenuItemService, Depends(get_menu_item_service)]
)-> BaseMenuItem | MenuItemNotFound:
    try:
        return await item_service.get_one_item(id)
    except MenuItemNotExists:
        response.status_code = status.HTTP_404_NOT_FOUND
        return MenuItemNotFound()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_menu_item(
        menu_item: BaseMenuItem,
        item_service: Annotated[MenuItemService, Depends(get_menu_item_service)]
        ):
        print("this is my menu item ")
        menu_item_id = await item_service.add_item(menu_item)
        return menu_item_id