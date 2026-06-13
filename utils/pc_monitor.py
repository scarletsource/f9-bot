import asyncio

from langame_api import get_pc_linking


async def monitor_pcs():

    while True:

        try:

            data = get_pc_linking()

            print()
            print("========== ПК КЛУБА ==========")

            for pc in data["data"]:

                print(
                    pc["name"],
                    pc["UUID"]
                )

            print("=============================")
            print()

        except Exception as e:

            print("ОШИБКА МОНИТОРА:", e)

        await asyncio.sleep(5)
