drop database if exists stenography;
create database stenography;
use stenography;

create table ranks (
  word varchar(50) primary key,
  rank_ int not null
  # foreign key (word) references words(word)
);
create table frequencies (
  word varchar(50) primary key,
  frequency int not null
  # foreign key (word) references words(word)
);
create table syllables (
  word varchar(50),
  syllable varchar(50) not null ,
  position int not null,
  primary key(word, syllable)
  # foreign key (word) references words(word)
);
create table phonemes (
  word varchar(50),
  phoneme nchar(50) not null,
  primary key(word, phoneme)
  # foreign key (word) references words(word)
);

# select * from words_phonemes
select count(*) from ranks;
# select count(*) from words;
select count(*) from phonemes;
select count(*) from syllables;
# select w.word from  words w  where w.word not in (select word from phonemes)
# delete from words w where word not in (select word from phonemes)
