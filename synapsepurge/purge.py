""" The main file """
import asyncio
import time
from random import randint

from nio import AsyncClient, responses

from synapsepurge import config, roomlist

async def purge(my_config: config.Config, client: AsyncClient, rooms: tuple):

    purge_config = my_config.values[config.PURGE_SECTION]
    synapse_config = my_config.values[config.SYNAPSE_SECTION]

    now = int(time.time())

    # The API expects milliseconds
    ts_to_purge = (now - (purge_config[config.PURGE_KEEP_DAYS] * 60 * 60 *24)) * 1000

    response = await client.login(password=synapse_config[config.SYNAPSE_PASSWORD], device_name=synapse_config[config.SYNAPSE_DEVICE_NAME])
    if isinstance(response, responses.LoginError):
        print("Unable to login: {}".format(response.message))
        await client.close()
        return

    semaphore = asyncio.Semaphore(purge_config[config.PURGE_MAX_JOBS])

    async def purge_worker(room: str):
        async with semaphore:
            start_time = time.time_ns()
            wait_time = randint(1,10)
            await asyncio.sleep(wait_time)
            end_time = time.time_ns()
            print("Room: {} finished: {} seconds".format(room, (end_time - start_time) / 1e9))

    tasks = [ asyncio.ensure_future(purge_worker(room[0])) for room in rooms]

    await asyncio.gather(*tasks)

    if client.logged_in:
        await client.logout()
    await client.close()

def main():
    my_config = config.Config()
    error = my_config.read_config()
    if error:
        print(error)
        exit(1)

    rooms = roomlist.get_rooms(my_config)

    synapse_values = my_config.values[config.SYNAPSE_SECTION]
    matrix_client = AsyncClient(homeserver=synapse_values[config.SYNAPSE_URL],
                                user=synapse_values[config.SYNAPSE_USERNAME])

    asyncio.get_event_loop().run_until_complete(purge(my_config, matrix_client, rooms))


if __name__ == '__main__':
    main()
