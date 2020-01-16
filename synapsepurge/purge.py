""" The main file """
import asyncio

from nio import AsyncClient, responses

from synapsepurge import config

async def purge(my_config: config.Config, client: AsyncClient, rooms: tuple):

    for room in rooms:
        print(room[0])

    response = await client.login(password=my_config.values[config.SYNAPSE_SECTION][config.SYNAPSE_PASSWORD], device_name=my_config.values[config.SYNAPSE_SECTION][config.SYNAPSE_DEVICE_NAME])
    if isinstance(response, responses.LoginError):
        print("Unable to login: {}".format(response.message))
    
    if client.logged_in:
        await client.logout()
    await client.close()

def main():
    my_config = config.Config()
    error = my_config.read_config()
    if error:
        print(error)
        exit(1)

    # rooms = roomlist.get_rooms(my_config)
    rooms = [("!OSdHmmGFxBlYdPldqA:matrix.org",)]

    synapse_values = my_config.values[config.SYNAPSE_SECTION]
    matrix_client = AsyncClient(homeserver=synapse_values[config.SYNAPSE_URL],
                                user=synapse_values[config.SYNAPSE_USERNAME])

    asyncio.get_event_loop().run_until_complete(purge(my_config, matrix_client, rooms))


if __name__ == '__main__':
    main()
