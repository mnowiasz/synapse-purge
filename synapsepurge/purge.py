""" The main file """
import asyncio
import time

from nio import AsyncClient, responses, Api

from synapsepurge import config, roomlist

_PURGE_HISTORY = "/_synapse/admin/v1/purge_history/{}"
_PURGE_HISTORY_STATUS = "/_synapse/admin/v1/purge_history_status/{}"


async def purge(my_config: config.Config, client: AsyncClient, rooms: tuple):
    purge_config = my_config.values[config.PURGE_SECTION]
    synapse_config = my_config.values[config.SYNAPSE_SECTION]

    now = int(time.time())

    # The API expects milliseconds
    ts_to_purge = (now - (purge_config[config.PURGE_KEEP_DAYS] * 60 * 60 * 24)) * 1000

    response = await client.login(password=synapse_config[config.SYNAPSE_PASSWORD],
                                  device_name=synapse_config[config.SYNAPSE_DEVICE_NAME])
    if isinstance(response, responses.LoginError):
        print("Unable to login: {}".format(response.message))
        await client.close()
        return

    semaphore = asyncio.Semaphore(purge_config[config.PURGE_MAX_JOBS])

    # The worker, sending purge requests and waiting for them to complete
    async def purge_worker(room: str):
        async with semaphore:
            start_time = time.time_ns()
            wait_time = purge_config[config.PURGE_WAIT_SECONDS]
            return_string = "OK"
            content = { "purge_up_to_ts": ts_to_purge }
            if purge_config[config.PURGE_DELETE_LOCAL_EVENTS]:
                content["delete_local_events"] = True

            headers = {"Content-type": "application/json",
                       "Authorization": "Bearer {}".format(client.access_token)}

            history_response = await client.send("POST", _PURGE_HISTORY.format(room), Api.to_json(content),
                                                 headers=headers)
            status_code = history_response.status
            if status_code != 200:
                return_string = "Error: {} {}".format(status_code, history_response.reason)
            else:
                purge_id = (await history_response.json())['purge_id']

                # Wait for the purge request to finish
                while True:
                    history_status_response = await client.send("GET", _PURGE_HISTORY_STATUS.format(purge_id),
                                                                headers=headers)
                    history_status_dict = await history_status_response.json()
                    history_status_purge = history_status_dict["status"]
                    if history_status_purge == "active":
                        await asyncio.sleep(wait_time)
                        continue
                    elif history_status_purge == "failed":
                        return_string = "Failed!"
                    elif history_status_purge != "complete":
                        return_string = "Unknown status: {}".format(history_status_purge)
                    break

            end_time = time.time_ns()
            print("Room: {} finished: {} ({} seconds)".format(room, return_string, (end_time - start_time) / 1e9))

    tasks = [asyncio.ensure_future(purge_worker(room[0])) for room in rooms]

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
