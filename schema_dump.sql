--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: animalprofile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.animalprofile (
    profile_id integer NOT NULL,
    animal_id integer,
    diet character varying(100),
    lifespan character varying(50),
    behavior text,
    fun_fact text,
    name character varying(50) NOT NULL,
    gender character varying(10) NOT NULL
);


ALTER TABLE public.animalprofile OWNER TO postgres;

--
-- Name: animalprofile_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.animalprofile_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animalprofile_profile_id_seq OWNER TO postgres;

--
-- Name: animalprofile_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.animalprofile_profile_id_seq OWNED BY public.animalprofile.profile_id;


--
-- Name: animals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.animals (
    animal_id integer NOT NULL,
    habitat_id integer,
    common_name character varying(100) NOT NULL,
    scientific_name character varying(100),
    status character varying(50)
);


ALTER TABLE public.animals OWNER TO postgres;

--
-- Name: animals_animal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.animals_animal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animals_animal_id_seq OWNER TO postgres;

--
-- Name: animals_animal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.animals_animal_id_seq OWNED BY public.animals.animal_id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    category_id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_category_id_seq OWNER TO postgres;

--
-- Name: categories_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_category_id_seq OWNED BY public.categories.category_id;


--
-- Name: enrichment_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enrichment_log (
    id integer NOT NULL,
    user_id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    animal_group text NOT NULL,
    enrichment_response text NOT NULL,
    individual_name text DEFAULT 'All'::text NOT NULL,
    enrichment_type text NOT NULL,
    enrichment_details text NOT NULL,
    time_in time without time zone NOT NULL,
    time_out time without time zone NOT NULL,
    observation_type text
);


ALTER TABLE public.enrichment_log OWNER TO postgres;

--
-- Name: enrichment_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.enrichment_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrichment_log_id_seq OWNER TO postgres;

--
-- Name: enrichment_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.enrichment_log_id_seq OWNED BY public.enrichment_log.id;


--
-- Name: feeding_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.feeding_logs (
    id integer NOT NULL,
    user_id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    animal_group text NOT NULL,
    individual_name text DEFAULT 'All'::text NOT NULL,
    food_type text NOT NULL,
    amount_fed text NOT NULL,
    observation_type text NOT NULL,
    leftover_food text,
    deer_feed_scoops integer,
    meds_added boolean DEFAULT false NOT NULL,
    individual_notes text,
    med_log_id integer DEFAULT 0 NOT NULL,
    nebraska text DEFAULT '0'::text NOT NULL,
    chicken text DEFAULT '0'::text NOT NULL,
    wholeprey text DEFAULT '0'::text NOT NULL,
    fruits text DEFAULT '0'::text NOT NULL,
    vegetables text DEFAULT '0'::text NOT NULL,
    fish text DEFAULT '0'::text NOT NULL,
    mazuri text DEFAULT '0'::text NOT NULL,
    total_food_quantity text DEFAULT '0'::text NOT NULL
);


ALTER TABLE public.feeding_logs OWNER TO postgres;

--
-- Name: feeding_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.feeding_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feeding_logs_id_seq OWNER TO postgres;

--
-- Name: feeding_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.feeding_logs_id_seq OWNED BY public.feeding_logs.id;


--
-- Name: habitat; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.habitat (
    habitat_id integer NOT NULL,
    habitat_name character varying(100) NOT NULL,
    description text,
    location character varying(100),
    size character varying(50)
);


ALTER TABLE public.habitat OWNER TO postgres;

--
-- Name: habitat_habitat_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.habitat_habitat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.habitat_habitat_id_seq OWNER TO postgres;

--
-- Name: habitat_habitat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.habitat_habitat_id_seq OWNED BY public.habitat.habitat_id;


--
-- Name: habitat_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.habitat_log (
    id integer NOT NULL,
    user_id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    animal_group text NOT NULL,
    observation_type text NOT NULL,
    habitat text NOT NULL,
    findings text NOT NULL,
    desc_of_cleaning text NOT NULL,
    pad_cleaning boolean DEFAULT false,
    water_change boolean DEFAULT false,
    pond_cleaning boolean DEFAULT false,
    waste_removal boolean DEFAULT false,
    brush_removal boolean DEFAULT false,
    fence_maintenance boolean DEFAULT false
);


ALTER TABLE public.habitat_log OWNER TO postgres;

--
-- Name: habitat_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.habitat_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.habitat_log_id_seq OWNER TO postgres;

--
-- Name: habitat_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.habitat_log_id_seq OWNED BY public.habitat_log.id;


--
-- Name: injury_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.injury_log (
    id integer NOT NULL,
    user_id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    animal_group text NOT NULL,
    individual_name text NOT NULL,
    encounter_type text NOT NULL,
    injury_type text NOT NULL,
    injury_desc text NOT NULL,
    exam_type text
);


ALTER TABLE public.injury_log OWNER TO postgres;

--
-- Name: injury_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.injury_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.injury_log_id_seq OWNER TO postgres;

--
-- Name: injury_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.injury_log_id_seq OWNED BY public.injury_log.id;


--
-- Name: med_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.med_log (
    id integer NOT NULL,
    user_id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    animal_group text NOT NULL,
    individual_name text NOT NULL,
    encounter_type text NOT NULL,
    med_type text NOT NULL,
    dose text NOT NULL,
    administration_route text NOT NULL,
    meds_taken boolean DEFAULT true NOT NULL,
    meloxicam boolean DEFAULT false,
    cephalexin boolean DEFAULT false,
    gabapentin boolean DEFAULT false,
    bravecto boolean DEFAULT false,
    intercepter boolean DEFAULT false,
    meloxicam_dose text DEFAULT '0'::text,
    cephalexin_dose text DEFAULT '0'::text,
    gabapentin_dose text DEFAULT '0'::text,
    bravecto_dose text DEFAULT '0'::text,
    intercepter_dose text DEFAULT '0'::text,
    ifother boolean DEFAULT false
);


ALTER TABLE public.med_log OWNER TO postgres;

--
-- Name: med_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.med_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.med_log_id_seq OWNER TO postgres;

--
-- Name: med_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.med_log_id_seq OWNED BY public.med_log.id;


--
-- Name: med_log_main; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.med_log_main (
    id integer NOT NULL,
    user_id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    animal_group text NOT NULL,
    individual_name text NOT NULL,
    encounter_type text NOT NULL,
    tied_to_injury boolean DEFAULT false NOT NULL,
    injury_id integer DEFAULT 0 NOT NULL,
    animal_sedated boolean DEFAULT false NOT NULL,
    sedation_id integer DEFAULT 0 NOT NULL,
    vet_notified boolean DEFAULT false NOT NULL,
    vet_response text NOT NULL,
    meds_given boolean DEFAULT false NOT NULL,
    med_id integer DEFAULT 0 NOT NULL,
    med_notes text
);


ALTER TABLE public.med_log_main OWNER TO postgres;

--
-- Name: med_log_main_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.med_log_main_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.med_log_main_id_seq OWNER TO postgres;

--
-- Name: med_log_main_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.med_log_main_id_seq OWNED BY public.med_log_main.id;


--
-- Name: note_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.note_categories (
    note_category_id integer NOT NULL,
    note_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.note_categories OWNER TO postgres;

--
-- Name: note_categories_note_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.note_categories_note_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.note_categories_note_category_id_seq OWNER TO postgres;

--
-- Name: note_categories_note_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.note_categories_note_category_id_seq OWNED BY public.note_categories.note_category_id;


--
-- Name: note_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.note_tags (
    note_tag_id integer NOT NULL,
    note_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.note_tags OWNER TO postgres;

--
-- Name: note_tags_note_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.note_tags_note_tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.note_tags_note_tag_id_seq OWNER TO postgres;

--
-- Name: note_tags_note_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.note_tags_note_tag_id_seq OWNED BY public.note_tags.note_tag_id;


--
-- Name: notes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notes (
    note_id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying(255) NOT NULL,
    content text,
    category character varying(255),
    is_shared boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_pinned boolean DEFAULT true
);


ALTER TABLE public.notes OWNER TO postgres;

--
-- Name: notes_note_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notes_note_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notes_note_id_seq OWNER TO postgres;

--
-- Name: notes_note_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notes_note_id_seq OWNED BY public.notes.note_id;


--
-- Name: reminders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reminders (
    id integer NOT NULL,
    user_id integer NOT NULL,
    date date NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    assigned_to integer,
    priority character varying(10) DEFAULT 'Medium'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT reminders_priority_check CHECK (((priority)::text = ANY ((ARRAY['High'::character varying, 'Medium'::character varying, 'Low'::character varying])::text[])))
);


ALTER TABLE public.reminders OWNER TO postgres;

--
-- Name: reminders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reminders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reminders_id_seq OWNER TO postgres;

--
-- Name: reminders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reminders_id_seq OWNED BY public.reminders.id;


--
-- Name: sedation_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sedation_log (
    id integer NOT NULL,
    user_id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    animal_group text NOT NULL,
    individual_name text NOT NULL,
    encounter_type text NOT NULL,
    sedation_med text NOT NULL,
    dose text NOT NULL,
    sedation_kit text,
    sedation_route text NOT NULL,
    time_in time without time zone NOT NULL,
    time_out time without time zone NOT NULL
);


ALTER TABLE public.sedation_log OWNER TO postgres;

--
-- Name: sedation_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sedation_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sedation_log_id_seq OWNER TO postgres;

--
-- Name: sedation_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sedation_log_id_seq OWNED BY public.sedation_log.id;


--
-- Name: shared_notes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shared_notes (
    shared_note_id integer NOT NULL,
    note_id integer NOT NULL,
    shared_with_user_id integer NOT NULL
);


ALTER TABLE public.shared_notes OWNER TO postgres;

--
-- Name: shared_notes_shared_note_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shared_notes_shared_note_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shared_notes_shared_note_id_seq OWNER TO postgres;

--
-- Name: shared_notes_shared_note_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shared_notes_shared_note_id_seq OWNED BY public.shared_notes.shared_note_id;


--
-- Name: tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    note_id integer NOT NULL,
    tag_name character varying(255) NOT NULL
);


ALTER TABLE public.tags OWNER TO postgres;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tags_id_seq OWNER TO postgres;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    role character varying(20) DEFAULT 'user'::character varying,
    active boolean DEFAULT true
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: vet_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vet_log (
    id integer NOT NULL,
    user_id integer NOT NULL,
    datetime timestamp without time zone NOT NULL,
    animal_group text NOT NULL,
    individual_name text NOT NULL,
    vet_name text NOT NULL,
    check_type text NOT NULL,
    vet_location text NOT NULL,
    vet_notes text
);


ALTER TABLE public.vet_log OWNER TO postgres;

--
-- Name: vet_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vet_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vet_log_id_seq OWNER TO postgres;

--
-- Name: vet_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vet_log_id_seq OWNED BY public.vet_log.id;


--
-- Name: animalprofile profile_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animalprofile ALTER COLUMN profile_id SET DEFAULT nextval('public.animalprofile_profile_id_seq'::regclass);


--
-- Name: animals animal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animals ALTER COLUMN animal_id SET DEFAULT nextval('public.animals_animal_id_seq'::regclass);


--
-- Name: categories category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN category_id SET DEFAULT nextval('public.categories_category_id_seq'::regclass);


--
-- Name: enrichment_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrichment_log ALTER COLUMN id SET DEFAULT nextval('public.enrichment_log_id_seq'::regclass);


--
-- Name: feeding_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feeding_logs ALTER COLUMN id SET DEFAULT nextval('public.feeding_logs_id_seq'::regclass);


--
-- Name: habitat habitat_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habitat ALTER COLUMN habitat_id SET DEFAULT nextval('public.habitat_habitat_id_seq'::regclass);


--
-- Name: habitat_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habitat_log ALTER COLUMN id SET DEFAULT nextval('public.habitat_log_id_seq'::regclass);


--
-- Name: injury_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.injury_log ALTER COLUMN id SET DEFAULT nextval('public.injury_log_id_seq'::regclass);


--
-- Name: med_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.med_log ALTER COLUMN id SET DEFAULT nextval('public.med_log_id_seq'::regclass);


--
-- Name: med_log_main id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.med_log_main ALTER COLUMN id SET DEFAULT nextval('public.med_log_main_id_seq'::regclass);


--
-- Name: note_categories note_category_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note_categories ALTER COLUMN note_category_id SET DEFAULT nextval('public.note_categories_note_category_id_seq'::regclass);


--
-- Name: note_tags note_tag_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note_tags ALTER COLUMN note_tag_id SET DEFAULT nextval('public.note_tags_note_tag_id_seq'::regclass);


--
-- Name: notes note_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notes ALTER COLUMN note_id SET DEFAULT nextval('public.notes_note_id_seq'::regclass);


--
-- Name: reminders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminders ALTER COLUMN id SET DEFAULT nextval('public.reminders_id_seq'::regclass);


--
-- Name: sedation_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sedation_log ALTER COLUMN id SET DEFAULT nextval('public.sedation_log_id_seq'::regclass);


--
-- Name: shared_notes shared_note_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_notes ALTER COLUMN shared_note_id SET DEFAULT nextval('public.shared_notes_shared_note_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: vet_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vet_log ALTER COLUMN id SET DEFAULT nextval('public.vet_log_id_seq'::regclass);


--
-- Name: animalprofile animalprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animalprofile
    ADD CONSTRAINT animalprofile_pkey PRIMARY KEY (profile_id);


--
-- Name: animals animals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animals
    ADD CONSTRAINT animals_pkey PRIMARY KEY (animal_id);


--
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);


--
-- Name: enrichment_log enrichment_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enrichment_log
    ADD CONSTRAINT enrichment_log_pkey PRIMARY KEY (id);


--
-- Name: feeding_logs feeding_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.feeding_logs
    ADD CONSTRAINT feeding_logs_pkey PRIMARY KEY (id);


--
-- Name: habitat_log habitat_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habitat_log
    ADD CONSTRAINT habitat_log_pkey PRIMARY KEY (id);


--
-- Name: habitat habitat_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habitat
    ADD CONSTRAINT habitat_pkey PRIMARY KEY (habitat_id);


--
-- Name: injury_log injury_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.injury_log
    ADD CONSTRAINT injury_log_pkey PRIMARY KEY (id);


--
-- Name: med_log_main med_log_main_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.med_log_main
    ADD CONSTRAINT med_log_main_pkey PRIMARY KEY (id);


--
-- Name: med_log med_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.med_log
    ADD CONSTRAINT med_log_pkey PRIMARY KEY (id);


--
-- Name: note_categories note_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note_categories
    ADD CONSTRAINT note_categories_pkey PRIMARY KEY (note_category_id);


--
-- Name: note_tags note_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note_tags
    ADD CONSTRAINT note_tags_pkey PRIMARY KEY (note_tag_id);


--
-- Name: notes notes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (note_id);


--
-- Name: reminders reminders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reminders
    ADD CONSTRAINT reminders_pkey PRIMARY KEY (id);


--
-- Name: sedation_log sedation_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sedation_log
    ADD CONSTRAINT sedation_log_pkey PRIMARY KEY (id);


--
-- Name: shared_notes shared_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_notes
    ADD CONSTRAINT shared_notes_pkey PRIMARY KEY (shared_note_id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: vet_log vet_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vet_log
    ADD CONSTRAINT vet_log_pkey PRIMARY KEY (id);


--
-- Name: idx_notes_search; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_notes_search ON public.notes USING btree (title, content);


--
-- Name: animalprofile animalprofile_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animalprofile
    ADD CONSTRAINT animalprofile_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animals(animal_id);


--
-- Name: animals animals_habitat_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.animals
    ADD CONSTRAINT animals_habitat_id_fkey FOREIGN KEY (habitat_id) REFERENCES public.habitat(habitat_id);


--
-- Name: note_categories note_categories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note_categories
    ADD CONSTRAINT note_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(category_id) ON DELETE CASCADE;


--
-- Name: note_categories note_categories_note_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note_categories
    ADD CONSTRAINT note_categories_note_id_fkey FOREIGN KEY (note_id) REFERENCES public.notes(note_id) ON DELETE CASCADE;


--
-- Name: note_tags note_tags_note_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note_tags
    ADD CONSTRAINT note_tags_note_id_fkey FOREIGN KEY (note_id) REFERENCES public.notes(note_id) ON DELETE CASCADE;


--
-- Name: note_tags note_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.note_tags
    ADD CONSTRAINT note_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- Name: notes notes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: shared_notes shared_notes_note_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_notes
    ADD CONSTRAINT shared_notes_note_id_fkey FOREIGN KEY (note_id) REFERENCES public.notes(note_id) ON DELETE CASCADE;


--
-- Name: shared_notes shared_notes_shared_with_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shared_notes
    ADD CONSTRAINT shared_notes_shared_with_user_id_fkey FOREIGN KEY (shared_with_user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: tags tags_note_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_note_id_fkey FOREIGN KEY (note_id) REFERENCES public.notes(note_id) ON DELETE CASCADE;


--
-- Name: TABLE pg_aggregate; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_aggregate TO bays_owner;


--
-- Name: TABLE pg_am; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_am TO bays_owner;


--
-- Name: TABLE pg_amop; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_amop TO bays_owner;


--
-- Name: TABLE pg_amproc; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_amproc TO bays_owner;


--
-- Name: TABLE pg_attrdef; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_attrdef TO bays_owner;


--
-- Name: TABLE pg_attribute; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_attribute TO bays_owner;


--
-- Name: TABLE pg_auth_members; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_auth_members TO bays_owner;


--
-- Name: TABLE pg_authid; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_authid TO bays_owner;


--
-- Name: TABLE pg_available_extension_versions; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_available_extension_versions TO bays_owner;


--
-- Name: TABLE pg_available_extensions; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_available_extensions TO bays_owner;


--
-- Name: TABLE pg_backend_memory_contexts; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_backend_memory_contexts TO bays_owner;


--
-- Name: TABLE pg_cast; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_cast TO bays_owner;


--
-- Name: TABLE pg_class; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_class TO bays_owner;


--
-- Name: TABLE pg_collation; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_collation TO bays_owner;


--
-- Name: TABLE pg_config; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_config TO bays_owner;


--
-- Name: TABLE pg_constraint; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_constraint TO bays_owner;


--
-- Name: TABLE pg_conversion; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_conversion TO bays_owner;


--
-- Name: TABLE pg_cursors; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_cursors TO bays_owner;


--
-- Name: TABLE pg_database; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_database TO bays_owner;


--
-- Name: TABLE pg_db_role_setting; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_db_role_setting TO bays_owner;


--
-- Name: TABLE pg_default_acl; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_default_acl TO bays_owner;


--
-- Name: TABLE pg_depend; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_depend TO bays_owner;


--
-- Name: TABLE pg_description; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_description TO bays_owner;


--
-- Name: TABLE pg_enum; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_enum TO bays_owner;


--
-- Name: TABLE pg_event_trigger; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_event_trigger TO bays_owner;


--
-- Name: TABLE pg_extension; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_extension TO bays_owner;


--
-- Name: TABLE pg_file_settings; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_file_settings TO bays_owner;


--
-- Name: TABLE pg_foreign_data_wrapper; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_foreign_data_wrapper TO bays_owner;


--
-- Name: TABLE pg_foreign_server; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_foreign_server TO bays_owner;


--
-- Name: TABLE pg_foreign_table; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_foreign_table TO bays_owner;


--
-- Name: TABLE pg_group; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_group TO bays_owner;


--
-- Name: TABLE pg_hba_file_rules; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_hba_file_rules TO bays_owner;


--
-- Name: TABLE pg_ident_file_mappings; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_ident_file_mappings TO bays_owner;


--
-- Name: TABLE pg_index; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_index TO bays_owner;


--
-- Name: TABLE pg_indexes; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_indexes TO bays_owner;


--
-- Name: TABLE pg_inherits; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_inherits TO bays_owner;


--
-- Name: TABLE pg_init_privs; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_init_privs TO bays_owner;


--
-- Name: TABLE pg_language; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_language TO bays_owner;


--
-- Name: TABLE pg_largeobject; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_largeobject TO bays_owner;


--
-- Name: TABLE pg_largeobject_metadata; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_largeobject_metadata TO bays_owner;


--
-- Name: TABLE pg_locks; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_locks TO bays_owner;


--
-- Name: TABLE pg_matviews; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_matviews TO bays_owner;


--
-- Name: TABLE pg_namespace; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_namespace TO bays_owner;


--
-- Name: TABLE pg_opclass; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_opclass TO bays_owner;


--
-- Name: TABLE pg_operator; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_operator TO bays_owner;


--
-- Name: TABLE pg_opfamily; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_opfamily TO bays_owner;


--
-- Name: TABLE pg_parameter_acl; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_parameter_acl TO bays_owner;


--
-- Name: TABLE pg_partitioned_table; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_partitioned_table TO bays_owner;


--
-- Name: TABLE pg_policies; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_policies TO bays_owner;


--
-- Name: TABLE pg_policy; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_policy TO bays_owner;


--
-- Name: TABLE pg_prepared_statements; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_prepared_statements TO bays_owner;


--
-- Name: TABLE pg_prepared_xacts; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_prepared_xacts TO bays_owner;


--
-- Name: TABLE pg_proc; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_proc TO bays_owner;


--
-- Name: TABLE pg_publication; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_publication TO bays_owner;


--
-- Name: TABLE pg_publication_namespace; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_publication_namespace TO bays_owner;


--
-- Name: TABLE pg_publication_rel; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_publication_rel TO bays_owner;


--
-- Name: TABLE pg_publication_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_publication_tables TO bays_owner;


--
-- Name: TABLE pg_range; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_range TO bays_owner;


--
-- Name: TABLE pg_replication_origin; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_replication_origin TO bays_owner;


--
-- Name: TABLE pg_replication_origin_status; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_replication_origin_status TO bays_owner;


--
-- Name: TABLE pg_replication_slots; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_replication_slots TO bays_owner;


--
-- Name: TABLE pg_rewrite; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_rewrite TO bays_owner;


--
-- Name: TABLE pg_roles; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_roles TO bays_owner;


--
-- Name: TABLE pg_rules; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_rules TO bays_owner;


--
-- Name: TABLE pg_seclabel; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_seclabel TO bays_owner;


--
-- Name: TABLE pg_seclabels; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_seclabels TO bays_owner;


--
-- Name: TABLE pg_sequence; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_sequence TO bays_owner;


--
-- Name: TABLE pg_sequences; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_sequences TO bays_owner;


--
-- Name: TABLE pg_settings; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_settings TO bays_owner;


--
-- Name: TABLE pg_shadow; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_shadow TO bays_owner;


--
-- Name: TABLE pg_shdepend; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_shdepend TO bays_owner;


--
-- Name: TABLE pg_shdescription; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_shdescription TO bays_owner;


--
-- Name: TABLE pg_shmem_allocations; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_shmem_allocations TO bays_owner;


--
-- Name: TABLE pg_shseclabel; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_shseclabel TO bays_owner;


--
-- Name: TABLE pg_stat_activity; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_activity TO bays_owner;


--
-- Name: TABLE pg_stat_all_indexes; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_all_indexes TO bays_owner;


--
-- Name: TABLE pg_stat_all_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_all_tables TO bays_owner;


--
-- Name: TABLE pg_stat_archiver; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_archiver TO bays_owner;


--
-- Name: TABLE pg_stat_bgwriter; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_bgwriter TO bays_owner;


--
-- Name: TABLE pg_stat_checkpointer; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_checkpointer TO bays_owner;


--
-- Name: TABLE pg_stat_database; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_database TO bays_owner;


--
-- Name: TABLE pg_stat_database_conflicts; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_database_conflicts TO bays_owner;


--
-- Name: TABLE pg_stat_gssapi; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_gssapi TO bays_owner;


--
-- Name: TABLE pg_stat_io; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_io TO bays_owner;


--
-- Name: TABLE pg_stat_progress_analyze; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_progress_analyze TO bays_owner;


--
-- Name: TABLE pg_stat_progress_basebackup; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_progress_basebackup TO bays_owner;


--
-- Name: TABLE pg_stat_progress_cluster; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_progress_cluster TO bays_owner;


--
-- Name: TABLE pg_stat_progress_copy; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_progress_copy TO bays_owner;


--
-- Name: TABLE pg_stat_progress_create_index; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_progress_create_index TO bays_owner;


--
-- Name: TABLE pg_stat_progress_vacuum; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_progress_vacuum TO bays_owner;


--
-- Name: TABLE pg_stat_recovery_prefetch; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_recovery_prefetch TO bays_owner;


--
-- Name: TABLE pg_stat_replication; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_replication TO bays_owner;


--
-- Name: TABLE pg_stat_replication_slots; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_replication_slots TO bays_owner;


--
-- Name: TABLE pg_stat_slru; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_slru TO bays_owner;


--
-- Name: TABLE pg_stat_ssl; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_ssl TO bays_owner;


--
-- Name: TABLE pg_stat_subscription; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_subscription TO bays_owner;


--
-- Name: TABLE pg_stat_subscription_stats; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_subscription_stats TO bays_owner;


--
-- Name: TABLE pg_stat_sys_indexes; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_sys_indexes TO bays_owner;


--
-- Name: TABLE pg_stat_sys_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_sys_tables TO bays_owner;


--
-- Name: TABLE pg_stat_user_functions; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_user_functions TO bays_owner;


--
-- Name: TABLE pg_stat_user_indexes; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_user_indexes TO bays_owner;


--
-- Name: TABLE pg_stat_user_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_user_tables TO bays_owner;


--
-- Name: TABLE pg_stat_wal; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_wal TO bays_owner;


--
-- Name: TABLE pg_stat_wal_receiver; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_wal_receiver TO bays_owner;


--
-- Name: TABLE pg_stat_xact_all_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_xact_all_tables TO bays_owner;


--
-- Name: TABLE pg_stat_xact_sys_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_xact_sys_tables TO bays_owner;


--
-- Name: TABLE pg_stat_xact_user_functions; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_xact_user_functions TO bays_owner;


--
-- Name: TABLE pg_stat_xact_user_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stat_xact_user_tables TO bays_owner;


--
-- Name: TABLE pg_statio_all_indexes; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statio_all_indexes TO bays_owner;


--
-- Name: TABLE pg_statio_all_sequences; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statio_all_sequences TO bays_owner;


--
-- Name: TABLE pg_statio_all_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statio_all_tables TO bays_owner;


--
-- Name: TABLE pg_statio_sys_indexes; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statio_sys_indexes TO bays_owner;


--
-- Name: TABLE pg_statio_sys_sequences; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statio_sys_sequences TO bays_owner;


--
-- Name: TABLE pg_statio_sys_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statio_sys_tables TO bays_owner;


--
-- Name: TABLE pg_statio_user_indexes; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statio_user_indexes TO bays_owner;


--
-- Name: TABLE pg_statio_user_sequences; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statio_user_sequences TO bays_owner;


--
-- Name: TABLE pg_statio_user_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statio_user_tables TO bays_owner;


--
-- Name: TABLE pg_statistic; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statistic TO bays_owner;


--
-- Name: TABLE pg_statistic_ext; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statistic_ext TO bays_owner;


--
-- Name: TABLE pg_statistic_ext_data; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_statistic_ext_data TO bays_owner;


--
-- Name: TABLE pg_stats; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stats TO bays_owner;


--
-- Name: TABLE pg_stats_ext; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stats_ext TO bays_owner;


--
-- Name: TABLE pg_stats_ext_exprs; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_stats_ext_exprs TO bays_owner;


--
-- Name: TABLE pg_subscription; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_subscription TO bays_owner;


--
-- Name: TABLE pg_subscription_rel; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_subscription_rel TO bays_owner;


--
-- Name: TABLE pg_tables; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_tables TO bays_owner;


--
-- Name: TABLE pg_tablespace; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_tablespace TO bays_owner;


--
-- Name: TABLE pg_timezone_abbrevs; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_timezone_abbrevs TO bays_owner;


--
-- Name: TABLE pg_timezone_names; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_timezone_names TO bays_owner;


--
-- Name: TABLE pg_transform; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_transform TO bays_owner;


--
-- Name: TABLE pg_trigger; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_trigger TO bays_owner;


--
-- Name: TABLE pg_ts_config; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_ts_config TO bays_owner;


--
-- Name: TABLE pg_ts_config_map; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_ts_config_map TO bays_owner;


--
-- Name: TABLE pg_ts_dict; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_ts_dict TO bays_owner;


--
-- Name: TABLE pg_ts_parser; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_ts_parser TO bays_owner;


--
-- Name: TABLE pg_ts_template; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_ts_template TO bays_owner;


--
-- Name: TABLE pg_type; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_type TO bays_owner;


--
-- Name: TABLE pg_user; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_user TO bays_owner;


--
-- Name: TABLE pg_user_mapping; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_user_mapping TO bays_owner;


--
-- Name: TABLE pg_user_mappings; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_user_mappings TO bays_owner;


--
-- Name: TABLE pg_views; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_views TO bays_owner;


--
-- Name: TABLE pg_wait_events; Type: ACL; Schema: pg_catalog; Owner: postgres
--

GRANT ALL ON TABLE pg_catalog.pg_wait_events TO bays_owner;


--
-- Name: TABLE animalprofile; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.animalprofile TO bays_owner;


--
-- Name: SEQUENCE animalprofile_profile_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.animalprofile_profile_id_seq TO bays_owner;


--
-- Name: TABLE animals; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.animals TO bays_owner;


--
-- Name: SEQUENCE animals_animal_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.animals_animal_id_seq TO bays_owner;


--
-- Name: TABLE categories; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.categories TO bays_owner;


--
-- Name: SEQUENCE categories_category_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.categories_category_id_seq TO bays_owner;


--
-- Name: TABLE enrichment_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.enrichment_log TO bays_owner;


--
-- Name: SEQUENCE enrichment_log_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.enrichment_log_id_seq TO bays_owner;


--
-- Name: TABLE feeding_logs; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.feeding_logs TO bays_owner;


--
-- Name: SEQUENCE feeding_logs_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.feeding_logs_id_seq TO bays_owner;


--
-- Name: TABLE habitat; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.habitat TO bays_owner;


--
-- Name: SEQUENCE habitat_habitat_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.habitat_habitat_id_seq TO bays_owner;


--
-- Name: TABLE habitat_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.habitat_log TO bays_owner;


--
-- Name: SEQUENCE habitat_log_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.habitat_log_id_seq TO bays_owner;


--
-- Name: TABLE injury_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.injury_log TO bays_owner;


--
-- Name: SEQUENCE injury_log_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.injury_log_id_seq TO bays_owner;


--
-- Name: TABLE med_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.med_log TO bays_owner;


--
-- Name: SEQUENCE med_log_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.med_log_id_seq TO bays_owner;


--
-- Name: TABLE med_log_main; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.med_log_main TO bays_owner;


--
-- Name: SEQUENCE med_log_main_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.med_log_main_id_seq TO bays_owner;


--
-- Name: TABLE note_categories; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.note_categories TO bays_owner;


--
-- Name: SEQUENCE note_categories_note_category_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.note_categories_note_category_id_seq TO bays_owner;


--
-- Name: TABLE note_tags; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.note_tags TO bays_owner;


--
-- Name: SEQUENCE note_tags_note_tag_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.note_tags_note_tag_id_seq TO bays_owner;


--
-- Name: TABLE notes; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.notes TO bays_owner;


--
-- Name: SEQUENCE notes_note_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.notes_note_id_seq TO bays_owner;


--
-- Name: TABLE reminders; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.reminders TO bays_owner;


--
-- Name: SEQUENCE reminders_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.reminders_id_seq TO bays_owner;


--
-- Name: TABLE sedation_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.sedation_log TO bays_owner;


--
-- Name: SEQUENCE sedation_log_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.sedation_log_id_seq TO bays_owner;


--
-- Name: TABLE shared_notes; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.shared_notes TO bays_owner;


--
-- Name: SEQUENCE shared_notes_shared_note_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.shared_notes_shared_note_id_seq TO bays_owner;


--
-- Name: TABLE tags; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tags TO bays_owner;


--
-- Name: SEQUENCE tags_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.tags_id_seq TO bays_owner;


--
-- Name: TABLE users; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.users TO bays_owner;


--
-- Name: SEQUENCE users_user_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.users_user_id_seq TO bays_owner;


--
-- Name: TABLE vet_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.vet_log TO bays_owner;


--
-- Name: SEQUENCE vet_log_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON SEQUENCE public.vet_log_id_seq TO bays_owner;


--
-- PostgreSQL database dump complete
--

