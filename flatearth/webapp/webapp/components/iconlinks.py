from ..imports import *

def icon_btnlink(
    icon_name, 
    icon_path='',
    icon_height='1.75rem',
    icon_padding=0,
    button_variant='link',
    cls=rx.button,
    href='',
    icon_kwargs={},
    box_kwargs={},
    **button_kwargs):

    return rx.box(
        cls(
            rx.image(
                src=f'/{icon_name}.svg' if not icon_path else icon_path,
                height=icon_height,
                padding=icon_padding,
                # filter=ColorState.invert_filter,
                **icon_kwargs
            ),
            variant=button_variant,
            href=href,
            padding=0,
            margin=0,
            **button_kwargs
        ),
        padding_y=0,
        padding_x='.5rem',
        **box_kwargs
    )



def icon_button(icon_name, **kwargs):
    return icon_btnlink(icon_name, cls=rx.button, **kwargs)

def icon_link(icon_name, href='', **kwargs):
    return icon_btnlink(icon_name, href=href, cls=rx.link, **kwargs)
