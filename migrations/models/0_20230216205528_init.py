from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "esrb" (
    "code" VARCHAR(30) NOT NULL  PRIMARY KEY,
    "description" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "game" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(150) NOT NULL,
    "x_cloud" BOOL NOT NULL  DEFAULT False,
    "status" VARCHAR(50) NOT NULL,
    "date_added" DATE NOT NULL,
    "date_removed" DATE,
    "date_released" DATE NOT NULL,
    "x_exclusive" BOOL NOT NULL  DEFAULT False,
    "esrb_id" VARCHAR(30) REFERENCES "esrb" ("code") ON DELETE SET NULL
);
COMMENT ON COLUMN "game"."status" IS 'ACTIVE: Active\nCOMING_SOON: Coming soon\nREMOVED: Removed\nLEAVING_SOON: Leaving soon';
CREATE TABLE IF NOT EXISTS "genre" (
    "name" VARCHAR(50) NOT NULL  PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "system" (
    "name" VARCHAR(50) NOT NULL  PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "game_system" (
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE,
    "system_id" VARCHAR(50) NOT NULL REFERENCES "system" ("name") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "game_genre" (
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE,
    "genre_id" VARCHAR(50) NOT NULL REFERENCES "genre" ("name") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
