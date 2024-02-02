from ..imports import *
from reflex.components.chakra import ChakraComponent
from reflex.vars import Var


class BaseComponent(ChakraComponent):
    @classmethod
    def create(cls,*children,**props) -> rx.Component:
        return rx.Component(*children, **props)