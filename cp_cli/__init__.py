import click
from .listen import listen
from .execute import run

@click.group()
@click.pass_context
def main(ctx: click.Context):
    ctx.ensure_object(dict)

main.add_command(listen)
main.add_command(run)