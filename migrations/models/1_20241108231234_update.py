from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "message_history" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "user_id" BIGINT NOT NULL,
    "message" TEXT NOT NULL,
    "role" VARCHAR(6) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_message_his_user_id_ccaf1b" ON "message_history" ("user_id");
COMMENT ON COLUMN "message_history"."role" IS 'SYSTEM: system\nUSER: user';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "message_history";"""
