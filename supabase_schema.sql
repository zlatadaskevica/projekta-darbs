-- Supabase schema for Astronomy & Space Events Tracker

create table if not exists public.users (
    id bigint generated always as identity primary key,
    email text not null unique,
    username text not null,
    password_hash text not null,
    created_at timestamp with time zone default timezone('utc', now())
);

create table if not exists public.events (
    id bigint generated always as identity primary key,
    title text not null,
    description text,
    event_date date not null,
    event_type text not null,
    created_at timestamp with time zone default timezone('utc', now())
);

create table if not exists public.saved_events (
    id bigint generated always as identity primary key,
    user_id bigint not null references public.users(id) on delete cascade,
    event_id bigint not null references public.events(id) on delete cascade,
    created_at timestamp with time zone default timezone('utc', now()),
    unique(user_id, event_id)
);
