PGDMP                     	    z           sovellus    14.5    14.5     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16403    sovellus    DATABASE     f   CREATE DATABASE sovellus WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Finnish_Finland.1252';
    DROP DATABASE sovellus;
                postgres    false            �            1259    16407    users    TABLE     ]   CREATE TABLE public.users (
    id integer NOT NULL,
    username text,
    password text
);
    DROP TABLE public.users;
       public         heap    lassi    false            �            1259    16406    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          lassi    false    210            �           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          lassi    false    209            \           2604    16410    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          lassi    false    210    209    210            �          0    16407    users 
   TABLE DATA           7   COPY public.users (id, username, password) FROM stdin;
    public          lassi    false    210   �	       �           0    0    users_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.users_id_seq', 1, true);
          public          lassi    false    209            ^           2606    16414    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            lassi    false    210            �   s   x��9�0 �:~Gj�u��Ӆ���D���Br��a�e�n���ڬ��}Oi
��z�i?���8_��>%)�+0�	x�U�� 2`���!�9�(����B���s?�2 �     