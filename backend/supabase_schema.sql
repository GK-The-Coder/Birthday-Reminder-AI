create table if not exists public.users (
  id uuid primary key references auth.users(id) on delete cascade,
  name text not null,
  email text unique not null,
  password text,
  created_at timestamptz not null default now()
);

create table if not exists public.birthdays (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.users(id) on delete cascade,
  name text not null,
  email text not null,
  birthday date not null,
  created_at timestamptz not null default now()
);

create table if not exists public.email_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.users(id) on delete cascade,
  birthday_id uuid references public.birthdays(id) on delete set null,
  delivery_date date,
  name text not null,
  email text not null,
  status text not null,
  message text,
  timestamp timestamptz not null default now()
);

create index if not exists birthdays_user_id_idx
  on public.birthdays(user_id);

create index if not exists email_logs_user_id_idx
  on public.email_logs(user_id);

alter table public.email_logs add column if not exists birthday_id
  uuid references public.birthdays(id) on delete set null;
alter table public.email_logs add column if not exists delivery_date date;

create unique index if not exists email_logs_birthday_delivery_idx
  on public.email_logs(birthday_id, delivery_date)
  where birthday_id is not null and delivery_date is not null;

-- Existing installations may still have this unused custom-auth column.
alter table public.users alter column password drop not null;

alter table public.users enable row level security;
alter table public.birthdays enable row level security;
alter table public.email_logs enable row level security;

drop policy if exists "Users can view their own profile" on public.users;
create policy "Users can view their own profile"
  on public.users for select
  using (auth.uid() = id);

drop policy if exists "Users can create their own profile" on public.users;
create policy "Users can create their own profile"
  on public.users for insert
  with check (auth.uid() = id);

drop policy if exists "Users can update their own profile" on public.users;
create policy "Users can update their own profile"
  on public.users for update
  using (auth.uid() = id)
  with check (auth.uid() = id);

drop policy if exists "Users can manage their birthdays" on public.birthdays;
create policy "Users can manage their birthdays"
  on public.birthdays for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

drop policy if exists "Users can manage their email logs" on public.email_logs;
create policy "Users can manage their email logs"
  on public.email_logs for all
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
