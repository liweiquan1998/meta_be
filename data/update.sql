-- ----------------------------
-- SEQUENCE scene_id_seq for relation
-- ----------------------------
DROP SEQUENCE IF EXISTS scene_id_seq;

CREATE SEQUENCE scene_id_seq
START WITH 1
INCREMENT BY 1
NO MINVALUE
NO MAXVALUE
CACHE 1;

-- ----------------------------
-- Table structure for scene
-- ----------------------------
DROP TABLE IF EXISTS "public"."scene";
CREATE TABLE "public"."scene" (
  "id" int4 NOT NULL DEFAULT nextval('scene_id_seq'::regclass),
  "name" varchar(50) COLLATE "pg_catalog"."default",
  "thumbnail" varchar(255) COLLATE "pg_catalog"."default",
  "config_file" varchar(255) COLLATE "pg_catalog"."default",
  "tag" int4,
  "stage" int4,
  "base_id" int4,
  "store_id" int4,
  "create_id" int4,
  "create_time" int4,
  "update_id" int4,
  "update_time" int4
)
;
ALTER TABLE "public"."scene" OWNER TO "sxwldba";
COMMENT ON COLUMN "public"."scene"."id" IS '主键';
COMMENT ON COLUMN "public"."scene"."name" IS '场景名称';
COMMENT ON COLUMN "public"."scene"."thumbnail" IS '缩略图地址';
COMMENT ON COLUMN "public"."scene"."config_file" IS '配置文件';
COMMENT ON COLUMN "public"."scene"."tag" IS '标签（0：all，1：元商店，2：直播）';
COMMENT ON COLUMN "public"."scene"."stage" IS '阶段（0：硬装，1：软装，2：应用）';
COMMENT ON COLUMN "public"."scene"."base_id" IS '基础id';
COMMENT ON COLUMN "public"."scene"."store_id" IS '商家id';
COMMENT ON COLUMN "public"."scene"."create_id" IS '创建者id';
COMMENT ON COLUMN "public"."scene"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."scene"."update_id" IS '更新者id';
COMMENT ON COLUMN "public"."scene"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."scene" IS '场景';

-- ----------------------------
-- Primary Key structure for table scene
-- ----------------------------
ALTER TABLE "public"."scene" ADD CONSTRAINT "scene_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- SEQUENCE relation_id_seq for relation
-- ----------------------------
DROP SEQUENCE IF EXISTS relation_id_seq;

CREATE SEQUENCE relation_id_seq
START WITH 1
INCREMENT BY 1
NO MINVALUE
NO MAXVALUE
CACHE 1;

-- ----------------------------
-- Table structure for relation
-- ----------------------------
DROP TABLE IF EXISTS "public"."relation";
CREATE TABLE "public"."relation" (
  "id" int4 NOT NULL DEFAULT nextval('relation_id_seq'::regclass),
  "relation_type" varchar(20) COLLATE "pg_catalog"."default",
  "usage_scenario" varchar(20) COLLATE "pg_catalog"."default",
  "subject_id" int4,
  "entity_id" int4
)
;
ALTER TABLE "public"."relation" OWNER TO "sxwldba";
COMMENT ON COLUMN "public"."relation"."relation_type" IS '关系类型';
COMMENT ON COLUMN "public"."relation"."usage_scenario" IS '使用情景';
COMMENT ON COLUMN "public"."relation"."subject_id" IS '主体id：使用者';
COMMENT ON COLUMN "public"."relation"."entity_id" IS '实体id：被使用者';

-- ----------------------------
-- Primary Key structure for table relation
-- ----------------------------
ALTER TABLE "public"."relation" ADD CONSTRAINT "relation_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Update Add column for tts
-- ----------------------------
ALTER TABLE "public"."tts"
  ADD COLUMN "creator_id" int4;

COMMENT ON COLUMN "public"."tts"."creator_id" IS '创建者';