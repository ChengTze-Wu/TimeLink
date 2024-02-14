import click
from app.services import JWTService


"""
payload:
    name: optional,
    username: optional,
    email: optional,
    role: required: must be one of "admin", "group_owner", "group_member", "line_bot"
"""


@click.command("makejwt", help="Create JWT")
@click.option("--name", "-n", default=None)
@click.option("--username", "-u", default=None)
@click.option("--email", "-e", default=None)
@click.option(
    "--role",
    "-r",
    default=None,
    required=True,
    type=click.Choice(["admin", "group_owner", "group_member", "line_bot", "liff"]),
)
@click.option("--exp", "-x", type=int, default=None, help="Expire time in minutes")
def create_jwt(name, username, email, role, exp):
    jwt_service = JWTService()

    payload = {}
    if name:
        payload.update({"name": name})
    if username:
        payload.update({"username": username})
    if email:
        payload.update({"email": email})
    if role:
        payload.update({"role": role})
    if exp:
        jwt_service.set_exp_time(exp)

    access_token = jwt_service.generate(payload)

    click.echo(access_token)
