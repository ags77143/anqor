-- Run this entire file in your Supabase SQL Editor to set up the database

-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Lectures table: stores each uploaded lecture/video
create table lectures (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references auth.users(id) on delete cascade,
  title text not null,
  source_type text not null, -- 'youtube', 'transcript', 'pdf', 'pptx', 'txt'
  source_ref text, -- youtube URL or original filename
  raw_transcript text, -- the raw text that was processed
  created_at timestamptz default now()
);

-- Study materials table: stores all generated content per lecture
create table study_materials (
  id uuid primary key default uuid_generate_v4(),
  lecture_id uuid references lectures(id) on delete cascade,
  user_id uuid references auth.users(id) on delete cascade,
  summary text,
  notes text,
  glossary jsonb, -- array of {term, definition}
  quiz jsonb,     -- array of {question, options, answer, explanation}
  flashcards jsonb, -- array of {front, back}
  exam_topics text,
  created_at timestamptz default now()
);

-- Row Level Security: users can only see their own data
alter table lectures enable row level security;
alter table study_materials enable row level security;

create policy "Users see own lectures" on lectures
  for all using (auth.uid() = user_id);

create policy "Users see own materials" on study_materials
  for all using (auth.uid() = user_id);
