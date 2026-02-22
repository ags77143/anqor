-- Run this entire file in your Supabase SQL Editor
-- If you already ran the old schema, run just the subjects part at the bottom

create extension if not exists "uuid-ossp";

-- Subjects/folders table
create table if not exists subjects (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users(id) on delete cascade,
  name text not null,
  colour text default '#6c63ff',
  created_at timestamptz default now()
);

-- Lectures table (now with subject_id)
create table if not exists lectures (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users(id) on delete cascade,
  subject_id uuid references subjects(id) on delete set null,
  title text not null,
  source_type text not null,
  source_ref text,
  raw_transcript text,
  created_at timestamptz default now()
);

-- Study materials table
create table if not exists study_materials (
  id uuid primary key default uuid_generate_v4(),
  lecture_id uuid references lectures(id) on delete cascade,
  user_id uuid references auth.users(id) on delete cascade,
  summary text,
  notes text,
  glossary jsonb,
  quiz jsonb,
  flashcards jsonb,
  exam_topics text,
  created_at timestamptz default now()
);

-- Row Level Security
alter table subjects enable row level security;
alter table lectures enable row level security;
alter table study_materials enable row level security;

drop policy if exists "Users see own subjects" on subjects;
drop policy if exists "Users see own lectures" on lectures;
drop policy if exists "Users see own materials" on study_materials;

create policy "Users see own subjects" on subjects for all using (auth.uid() = user_id);
create policy "Users see own lectures" on lectures for all using (auth.uid() = user_id);
create policy "Users see own materials" on study_materials for all using (auth.uid() = user_id);
