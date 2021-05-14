from .spawnables import wanderer


def spawner(key):
    return {
        "SPAWN_WANDERER": wanderer.create_spawnable
    }.get(key)


def spawn(game, key, x, y):
    entity = spawner(key)(game)(x, y)
    entity.fire_event("spawned")
    return entity
