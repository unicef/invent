--
-- PostgreSQL database dump
--

-- Dumped from database version 10.4 (Debian 10.4-2.pgdg90+1)
-- Dumped by pg_dump version 10.4 (Debian 10.4-2.pgdg90+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.country_countryoffice DROP CONSTRAINT country_countryoffice_country_id_b3fd1b7d_fk_country_country_id;
ALTER TABLE ONLY public.country_countryoffice DROP CONSTRAINT country_countryoffic_regional_office_id_003499d9_fk_country_r;
DROP INDEX public.country_donor_name_pt_7ede7852_like;
DROP INDEX public.country_donor_name_fr_85295726_like;
DROP INDEX public.country_donor_name_es_25ba78ba_like;
DROP INDEX public.country_donor_name_en_27d38d97_like;
DROP INDEX public.country_donor_name_ar_c8972586_like;
DROP INDEX public.country_donor_name_7d1a1f44_like;
DROP INDEX public.country_donor_code_7786ec23_like;
DROP INDEX public.country_countryoffice_regional_office_id_003499d9;
DROP INDEX public.country_countryoffice_country_id_b3fd1b7d;
ALTER TABLE ONLY public.country_regionaloffice DROP CONSTRAINT country_regionaloffice_pkey;
ALTER TABLE ONLY public.country_donor DROP CONSTRAINT country_donor_pkey;
ALTER TABLE ONLY public.country_donor DROP CONSTRAINT country_donor_name_pt_key;
ALTER TABLE ONLY public.country_donor DROP CONSTRAINT country_donor_name_key;
ALTER TABLE ONLY public.country_donor DROP CONSTRAINT country_donor_name_fr_key;
ALTER TABLE ONLY public.country_donor DROP CONSTRAINT country_donor_name_es_key;
ALTER TABLE ONLY public.country_donor DROP CONSTRAINT country_donor_name_en_key;
ALTER TABLE ONLY public.country_donor DROP CONSTRAINT country_donor_name_ar_key;
ALTER TABLE ONLY public.country_donor DROP CONSTRAINT country_donor_code_7786ec23_uniq;
ALTER TABLE ONLY public.country_countryoffice DROP CONSTRAINT country_countryoffice_pkey;
ALTER TABLE public.country_regionaloffice ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.country_donor ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.country_countryoffice ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.country_regionaloffice_id_seq;
DROP TABLE public.country_regionaloffice;
DROP SEQUENCE public.country_donor_id_seq;
DROP TABLE public.country_donor;
DROP SEQUENCE public.country_countryoffice_id_seq;
DROP TABLE public.country_countryoffice;
SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: country_countryoffice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country_countryoffice (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(256) NOT NULL,
    name_en character varying(256),
    name_fr character varying(256),
    name_es character varying(256),
    name_pt character varying(256),
    name_ar character varying(256),
    region integer,
    country_id integer NOT NULL,
    regional_office_id integer,
    city character varying(256)
);


ALTER TABLE public.country_countryoffice OWNER TO postgres;

--
-- Name: country_countryoffice_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.country_countryoffice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.country_countryoffice_id_seq OWNER TO postgres;

--
-- Name: country_countryoffice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.country_countryoffice_id_seq OWNED BY public.country_countryoffice.id;


--
-- Name: country_donor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country_donor (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    name_en character varying(255),
    name_fr character varying(255),
    name_es character varying(255),
    name_pt character varying(255),
    logo character varying(100),
    cover character varying(100),
    cover_text text,
    footer_title character varying(128),
    footer_text character varying(128),
    code character varying(10) NOT NULL,
    name_ar character varying(255)
);


ALTER TABLE public.country_donor OWNER TO postgres;

--
-- Name: country_donor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.country_donor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.country_donor_id_seq OWNER TO postgres;

--
-- Name: country_donor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.country_donor_id_seq OWNED BY public.country_donor.id;


--
-- Name: country_regionaloffice; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country_regionaloffice (
    id integer NOT NULL,
    name character varying(256) NOT NULL
);


ALTER TABLE public.country_regionaloffice OWNER TO postgres;

--
-- Name: country_regionaloffice_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.country_regionaloffice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.country_regionaloffice_id_seq OWNER TO postgres;

--
-- Name: country_regionaloffice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.country_regionaloffice_id_seq OWNED BY public.country_regionaloffice.id;


--
-- Name: country_countryoffice id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_countryoffice ALTER COLUMN id SET DEFAULT nextval('public.country_countryoffice_id_seq'::regclass);


--
-- Name: country_donor id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_donor ALTER COLUMN id SET DEFAULT nextval('public.country_donor_id_seq'::regclass);


--
-- Name: country_regionaloffice id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_regionaloffice ALTER COLUMN id SET DEFAULT nextval('public.country_regionaloffice_id_seq'::regclass);


--
-- Data for Name: country_countryoffice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.country_countryoffice (id, created, modified, name, name_en, name_fr, name_es, name_pt, name_ar, region, country_id, regional_office_id, city) FROM stdin;
\.


--
-- Data for Name: country_donor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.country_donor (id, created, modified, name, name_en, name_fr, name_es, name_pt, logo, cover, cover_text, footer_title, footer_text, code, name_ar) FROM stdin;
\.


--
-- Data for Name: country_regionaloffice; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.country_regionaloffice (id, name) FROM stdin;
\.


--
-- Name: country_countryoffice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.country_countryoffice_id_seq', 1, false);


--
-- Name: country_donor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.country_donor_id_seq', 1, false);


--
-- Name: country_regionaloffice_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.country_regionaloffice_id_seq', 1, false);


--
-- Name: country_countryoffice country_countryoffice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_countryoffice
    ADD CONSTRAINT country_countryoffice_pkey PRIMARY KEY (id);


--
-- Name: country_donor country_donor_code_7786ec23_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_donor
    ADD CONSTRAINT country_donor_code_7786ec23_uniq UNIQUE (code);


--
-- Name: country_donor country_donor_name_ar_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_donor
    ADD CONSTRAINT country_donor_name_ar_key UNIQUE (name_ar);


--
-- Name: country_donor country_donor_name_en_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_donor
    ADD CONSTRAINT country_donor_name_en_key UNIQUE (name_en);


--
-- Name: country_donor country_donor_name_es_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_donor
    ADD CONSTRAINT country_donor_name_es_key UNIQUE (name_es);


--
-- Name: country_donor country_donor_name_fr_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_donor
    ADD CONSTRAINT country_donor_name_fr_key UNIQUE (name_fr);


--
-- Name: country_donor country_donor_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_donor
    ADD CONSTRAINT country_donor_name_key UNIQUE (name);


--
-- Name: country_donor country_donor_name_pt_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_donor
    ADD CONSTRAINT country_donor_name_pt_key UNIQUE (name_pt);


--
-- Name: country_donor country_donor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_donor
    ADD CONSTRAINT country_donor_pkey PRIMARY KEY (id);


--
-- Name: country_regionaloffice country_regionaloffice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_regionaloffice
    ADD CONSTRAINT country_regionaloffice_pkey PRIMARY KEY (id);


--
-- Name: country_countryoffice_country_id_b3fd1b7d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX country_countryoffice_country_id_b3fd1b7d ON public.country_countryoffice USING btree (country_id);


--
-- Name: country_countryoffice_regional_office_id_003499d9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX country_countryoffice_regional_office_id_003499d9 ON public.country_countryoffice USING btree (regional_office_id);


--
-- Name: country_donor_code_7786ec23_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX country_donor_code_7786ec23_like ON public.country_donor USING btree (code varchar_pattern_ops);


--
-- Name: country_donor_name_7d1a1f44_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX country_donor_name_7d1a1f44_like ON public.country_donor USING btree (name varchar_pattern_ops);


--
-- Name: country_donor_name_ar_c8972586_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX country_donor_name_ar_c8972586_like ON public.country_donor USING btree (name_ar varchar_pattern_ops);


--
-- Name: country_donor_name_en_27d38d97_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX country_donor_name_en_27d38d97_like ON public.country_donor USING btree (name_en varchar_pattern_ops);


--
-- Name: country_donor_name_es_25ba78ba_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX country_donor_name_es_25ba78ba_like ON public.country_donor USING btree (name_es varchar_pattern_ops);


--
-- Name: country_donor_name_fr_85295726_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX country_donor_name_fr_85295726_like ON public.country_donor USING btree (name_fr varchar_pattern_ops);


--
-- Name: country_donor_name_pt_7ede7852_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX country_donor_name_pt_7ede7852_like ON public.country_donor USING btree (name_pt varchar_pattern_ops);


--
-- Name: country_countryoffice country_countryoffic_regional_office_id_003499d9_fk_country_r; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_countryoffice
    ADD CONSTRAINT country_countryoffic_regional_office_id_003499d9_fk_country_r FOREIGN KEY (regional_office_id) REFERENCES public.country_regionaloffice(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: country_countryoffice country_countryoffice_country_id_b3fd1b7d_fk_country_country_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country_countryoffice
    ADD CONSTRAINT country_countryoffice_country_id_b3fd1b7d_fk_country_country_id FOREIGN KEY (country_id) REFERENCES public.country_country(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

