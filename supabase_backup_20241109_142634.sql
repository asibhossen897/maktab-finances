

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE EXTENSION IF NOT EXISTS "pgsodium" WITH SCHEMA "pgsodium";






COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "pg_graphql" WITH SCHEMA "graphql";






CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgjwt" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";





SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."admin_user" (
    "id" integer NOT NULL,
    "username" "text" NOT NULL,
    "password_hash" "bytea" NOT NULL
);


ALTER TABLE "public"."admin_user" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."admin_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."admin_user_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."admin_user_id_seq" OWNED BY "public"."admin_user"."id";



CREATE TABLE IF NOT EXISTS "public"."adminuser" (
    "id" integer NOT NULL,
    "username" character varying NOT NULL,
    "password_hash" "bytea" NOT NULL
);


ALTER TABLE "public"."adminuser" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."adminuser_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."adminuser_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."adminuser_id_seq" OWNED BY "public"."adminuser"."id";



CREATE TABLE IF NOT EXISTS "public"."donation" (
    "id" integer NOT NULL,
    "donor_name" "text" NOT NULL,
    "amount" double precision DEFAULT 0.0 NOT NULL,
    "date" "date" NOT NULL,
    "notes" "text",
    "is_anonymous" boolean DEFAULT false NOT NULL
);


ALTER TABLE "public"."donation" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."donation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."donation_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."donation_id_seq" OWNED BY "public"."donation"."id";



CREATE TABLE IF NOT EXISTS "public"."expense" (
    "id" integer NOT NULL,
    "description" "text" NOT NULL,
    "amount" double precision DEFAULT 0.0 NOT NULL,
    "date" "date" NOT NULL,
    "category" "text" NOT NULL
);


ALTER TABLE "public"."expense" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."expense_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."expense_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."expense_id_seq" OWNED BY "public"."expense"."id";



CREATE TABLE IF NOT EXISTS "public"."salary" (
    "id" integer NOT NULL,
    "teacher_name" "text" NOT NULL,
    "amount" double precision DEFAULT 0.0 NOT NULL,
    "date" "date" NOT NULL
);


ALTER TABLE "public"."salary" OWNER TO "postgres";


CREATE SEQUENCE IF NOT EXISTS "public"."salary_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "public"."salary_id_seq" OWNER TO "postgres";


ALTER SEQUENCE "public"."salary_id_seq" OWNED BY "public"."salary"."id";



ALTER TABLE ONLY "public"."admin_user" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."admin_user_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."adminuser" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."adminuser_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."donation" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."donation_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."expense" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."expense_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."salary" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."salary_id_seq"'::"regclass");



ALTER TABLE ONLY "public"."admin_user"
    ADD CONSTRAINT "admin_user_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."admin_user"
    ADD CONSTRAINT "admin_user_username_key" UNIQUE ("username");



ALTER TABLE ONLY "public"."adminuser"
    ADD CONSTRAINT "adminuser_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."adminuser"
    ADD CONSTRAINT "adminuser_username_key" UNIQUE ("username");



ALTER TABLE ONLY "public"."donation"
    ADD CONSTRAINT "donation_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."expense"
    ADD CONSTRAINT "expense_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."salary"
    ADD CONSTRAINT "salary_pkey" PRIMARY KEY ("id");





ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";


GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";



































































































































































































GRANT ALL ON TABLE "public"."admin_user" TO "anon";
GRANT ALL ON TABLE "public"."admin_user" TO "authenticated";
GRANT ALL ON TABLE "public"."admin_user" TO "service_role";



GRANT ALL ON SEQUENCE "public"."admin_user_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."admin_user_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."admin_user_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."adminuser" TO "anon";
GRANT ALL ON TABLE "public"."adminuser" TO "authenticated";
GRANT ALL ON TABLE "public"."adminuser" TO "service_role";



GRANT ALL ON SEQUENCE "public"."adminuser_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."adminuser_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."adminuser_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."donation" TO "anon";
GRANT ALL ON TABLE "public"."donation" TO "authenticated";
GRANT ALL ON TABLE "public"."donation" TO "service_role";



GRANT ALL ON SEQUENCE "public"."donation_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."donation_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."donation_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."expense" TO "anon";
GRANT ALL ON TABLE "public"."expense" TO "authenticated";
GRANT ALL ON TABLE "public"."expense" TO "service_role";



GRANT ALL ON SEQUENCE "public"."expense_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."expense_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."expense_id_seq" TO "service_role";



GRANT ALL ON TABLE "public"."salary" TO "anon";
GRANT ALL ON TABLE "public"."salary" TO "authenticated";
GRANT ALL ON TABLE "public"."salary" TO "service_role";



GRANT ALL ON SEQUENCE "public"."salary_id_seq" TO "anon";
GRANT ALL ON SEQUENCE "public"."salary_id_seq" TO "authenticated";
GRANT ALL ON SEQUENCE "public"."salary_id_seq" TO "service_role";



ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES  TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS  TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES  TO "service_role";






























RESET ALL;
