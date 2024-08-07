from search import es, crc_index_name, crc_mapping


async def create_es_indices():
    try:
        await es.create_index_if_not_exists(crc_index_name, crc_mapping)
        await es.list_all_indices()

    except Exception as e:
        print(e)


async def delete_es_index():
    try:
        await es.delete_index(crc_index_name)

    except Exception as e:
        print(e)
