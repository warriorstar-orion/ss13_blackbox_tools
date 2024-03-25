import json
import toml

# coding: utf-8
from sqlalchemy import CHAR, CheckConstraint, Column, Date, DateTime, Enum, Float, String, TIMESTAMP, Table, Text, Time, text, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, BIT, ENUM, INTEGER, LONGTEXT, MEDIUMINT, MEDIUMTEXT, SMALLINT, TINYINT, VARCHAR, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from request_mixin import make_cached_limiter_session

API_URL = "https://api.paradisestation.org/stats"

from typing import List

Base = declarative_base()
metadata = Base.metadata


class TwoFASecret(Base):
    __tablename__ = '2fa_secrets'

    ckey = Column(String(50), primary_key=True)
    secret = Column(String(64), nullable=False)
    date_setup = Column(DateTime, nullable=False, server_default=text("current_timestamp()"))
    last_time = Column(DateTime)


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(INTEGER(11), primary_key=True)
    ckey = Column(VARCHAR(32), nullable=False, index=True)
    admin_rank = Column(VARCHAR(32), nullable=False, server_default=text("'Administrator'"))
    level = Column(INTEGER(2), nullable=False, server_default=text("0"))
    flags = Column(INTEGER(16), nullable=False, server_default=text("0"))


class AdminLog(Base):
    __tablename__ = 'admin_log'

    id = Column(INTEGER(11), primary_key=True)
    datetime = Column(DateTime, nullable=False)
    adminckey = Column(VARCHAR(32), nullable=False, index=True)
    adminip = Column(VARCHAR(18), nullable=False)
    log = Column(MEDIUMTEXT, nullable=False)


class Ban(Base):
    __tablename__ = 'ban'

    id = Column(INTEGER(11), primary_key=True)
    bantime = Column(DateTime, nullable=False)
    ban_round_id = Column(INTEGER(11))
    serverip = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    server_id = Column(VARCHAR(50))
    bantype = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    reason = Column(MEDIUMTEXT, nullable=False)
    job = Column(String(32, 'utf8mb4_unicode_ci'))
    duration = Column(INTEGER(11), nullable=False)
    rounds = Column(INTEGER(11))
    expiration_time = Column(DateTime, nullable=False)
    ckey = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, index=True)
    computerid = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, index=True)
    ip = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, index=True)
    a_ckey = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    a_computerid = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    a_ip = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    who = Column(MEDIUMTEXT, nullable=False)
    adminwho = Column(MEDIUMTEXT, nullable=False)
    edits = Column(MEDIUMTEXT)
    unbanned = Column(TINYINT(1))
    unbanned_datetime = Column(DateTime)
    unbanned_round_id = Column(INTEGER(11))
    unbanned_ckey = Column(String(32, 'utf8mb4_unicode_ci'))
    unbanned_computerid = Column(String(32, 'utf8mb4_unicode_ci'))
    unbanned_ip = Column(String(32, 'utf8mb4_unicode_ci'))
    exportable = Column(TINYINT(4), nullable=False, index=True, server_default=text("1"))


class Changelog(Base):
    __tablename__ = 'changelog'

    id = Column(INTEGER(11), primary_key=True)
    pr_number = Column(INTEGER(11), nullable=False)
    date_merged = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
    author = Column(String(32), nullable=False)
    cl_type = Column(Enum('FIX', 'WIP', 'TWEAK', 'SOUNDADD', 'SOUNDDEL', 'CODEADD', 'CODEDEL', 'IMAGEADD', 'IMAGEDEL', 'SPELLCHECK', 'EXPERIMENT'), nullable=False)
    cl_entry = Column(Text, nullable=False)


class Character(Base):
    __tablename__ = 'characters'

    id = Column(INTEGER(11), primary_key=True)
    ckey = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, index=True)
    slot = Column(INTEGER(2), nullable=False)
    OOC_Notes = Column(LONGTEXT, nullable=False)
    real_name = Column(String(55, 'utf8mb4_unicode_ci'), nullable=False)
    name_is_always_random = Column(TINYINT(1), nullable=False)
    gender = Column(String(11, 'utf8mb4_unicode_ci'), nullable=False)
    age = Column(SMALLINT(4), nullable=False)
    species = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    language = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    hair_colour = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'#000000'"))
    secondary_hair_colour = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'#000000'"))
    facial_hair_colour = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'#000000'"))
    secondary_facial_hair_colour = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'#000000'"))
    skin_tone = Column(SMALLINT(4), nullable=False)
    skin_colour = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'#000000'"))
    marking_colours = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'head=%%23000000&body=%%23000000&tail=%%23000000'"))
    head_accessory_colour = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'#000000'"))
    hair_style_name = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    facial_style_name = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    marking_styles = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'head=None&body=None&tail=None'"))
    head_accessory_style_name = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    alt_head_name = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    eye_colour = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'#000000'"))
    underwear = Column(LONGTEXT, nullable=False)
    undershirt = Column(LONGTEXT, nullable=False)
    backbag = Column(LONGTEXT)
    b_type = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    alternate_option = Column(SMALLINT(4), nullable=False)
    job_support_high = Column(MEDIUMINT(8), nullable=False)
    job_support_med = Column(MEDIUMINT(8), nullable=False)
    job_support_low = Column(MEDIUMINT(8), nullable=False)
    job_medsci_high = Column(MEDIUMINT(8), nullable=False)
    job_medsci_med = Column(MEDIUMINT(8), nullable=False)
    job_medsci_low = Column(MEDIUMINT(8), nullable=False)
    job_engsec_high = Column(MEDIUMINT(8), nullable=False)
    job_engsec_med = Column(MEDIUMINT(8), nullable=False)
    job_engsec_low = Column(MEDIUMINT(8), nullable=False)
    flavor_text = Column(LONGTEXT, nullable=False)
    med_record = Column(LONGTEXT, nullable=False)
    sec_record = Column(LONGTEXT, nullable=False)
    gen_record = Column(LONGTEXT, nullable=False)
    disabilities = Column(MEDIUMINT(8), nullable=False)
    player_alt_titles = Column(LONGTEXT, nullable=False)
    organ_data = Column(LONGTEXT, nullable=False)
    rlimb_data = Column(LONGTEXT, nullable=False)
    nanotrasen_relation = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    speciesprefs = Column(INTEGER(1), nullable=False)
    socks = Column(LONGTEXT, nullable=False)
    body_accessory = Column(LONGTEXT, nullable=False)
    gear = Column(LONGTEXT, nullable=False)
    autohiss = Column(TINYINT(1), nullable=False)
    hair_gradient = Column(String(45, 'utf8mb4_unicode_ci'), nullable=False)
    hair_gradient_offset = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'0,0'"))
    hair_gradient_colour = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'#000000'"))
    hair_gradient_alpha = Column(TINYINT(3), nullable=False, server_default=text("255"))
    custom_emotes = Column(LONGTEXT)


class ConnectionLog(Base):
    __tablename__ = 'connection_log'

    id = Column(INTEGER(11), primary_key=True)
    datetime = Column(DateTime, nullable=False)
    ckey = Column(String(32), nullable=False, index=True)
    ip = Column(String(32), nullable=False, index=True)
    computerid = Column(String(32), nullable=False, index=True)
    server_id = Column(String(50))
    result = Column(Enum('ESTABLISHED', 'DROPPED - IPINTEL', 'DROPPED - BANNED', 'DROPPED - INVALID'), nullable=False, server_default=text("'ESTABLISHED'"))


class Customuseritem(Base):
    __tablename__ = 'customuseritems'

    id = Column(INTEGER(11), primary_key=True)
    cuiCKey = Column(String(36), nullable=False, index=True)
    cuiRealName = Column(String(60), nullable=False)
    cuiPath = Column(String(255), nullable=False)
    cuiItemName = Column(Text)
    cuiDescription = Column(Text)
    cuiReason = Column(Text)
    cuiPropAdjust = Column(Text)
    cuiJobMask = Column(Text, nullable=False)


class Death(Base):
    __tablename__ = 'death'

    id = Column(INTEGER(11), primary_key=True)
    pod = Column(Text, nullable=False, comment='Place of death')
    coord = Column(Text, nullable=False, comment='X, Y, Z POD')
    tod = Column(DateTime, nullable=False, comment='Time of death')
    death_rid = Column(INTEGER(11))
    server_id = Column(Text)
    job = Column(Text, nullable=False)
    special = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    byondkey = Column(Text, nullable=False)
    laname = Column(Text, nullable=False, comment='Last attacker name')
    lakey = Column(Text, nullable=False, comment='Last attacker key')
    gender = Column(Text, nullable=False)
    bruteloss = Column(INTEGER(11), nullable=False)
    brainloss = Column(INTEGER(11), nullable=False)
    fireloss = Column(INTEGER(11), nullable=False)
    oxyloss = Column(INTEGER(11), nullable=False)


class Donator(Base):
    __tablename__ = 'donators'

    patreon_name = Column(String(32, 'utf8mb4_unicode_ci'), primary_key=True)
    tier = Column(INTEGER(2))
    ckey = Column(String(32, 'utf8mb4_unicode_ci'), index=True, comment='Manual Field')
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    active = Column(TINYINT(1))


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(INTEGER(11), primary_key=True)
    datetime = Column(DateTime, nullable=False)
    round_id:Mapped[int] = mapped_column(ForeignKey("round.id"))
    key_name = Column(String(32), nullable=False)
    key_type = Column(Enum('text', 'amount', 'tally', 'nested tally', 'associative'), nullable=False)
    version = Column(TINYINT(3), nullable=False)
    json = Column(JSON, nullable=False)

    round:Mapped["Round"] = relationship(back_populates="feedbacks")

    def __str__(self):
        return f"<Fdbk Rnd#{self.round_id} {self.key_name}>"
    
    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        return self.json['data'].__getitem__(key)


class InstanceDataCache(Base):
    __tablename__ = 'instance_data_cache'

    server_id = Column(String(50), primary_key=True, nullable=False)
    key_name = Column(String(50), primary_key=True, nullable=False)
    key_value = Column(String(12345), nullable=False)
    last_updated = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class Ip2group(Base):
    __tablename__ = 'ip2group'

    ip = Column(VARCHAR(18), primary_key=True)
    date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    groupstr = Column(VARCHAR(32), nullable=False, index=True, server_default=text("''"))


class Ipintel(Base):
    __tablename__ = 'ipintel'

    ip = Column(INTEGER(10), primary_key=True)
    date = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    intel = Column(Float(asdecimal=True), nullable=False, server_default=text("0"))


class LegacyPopulation(Base):
    __tablename__ = 'legacy_population'

    id = Column(INTEGER(11), primary_key=True)
    playercount = Column(INTEGER(11))
    admincount = Column(INTEGER(11))
    server_id = Column(String(50))
    time = Column(DateTime, nullable=False)


class Library(Base):
    __tablename__ = 'library'

    id = Column(INTEGER(11), primary_key=True)
    author = Column(MEDIUMTEXT, nullable=False)
    title = Column(MEDIUMTEXT, nullable=False)
    content = Column(MEDIUMTEXT, nullable=False)
    ckey = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, index=True)
    reports = Column(MEDIUMTEXT, nullable=False, index=True)
    summary = Column(MEDIUMTEXT, nullable=False)
    rating = Column(Float(asdecimal=True), server_default=text("0"))
    raters = Column(MEDIUMTEXT, nullable=False)
    primary_category = Column(INTEGER(11), server_default=text("0"))
    secondary_category = Column(INTEGER(11), nullable=False, server_default=text("0"))
    tertiary_category = Column(INTEGER(11), server_default=text("0"))


class Memo(Base):
    __tablename__ = 'memo'

    ckey = Column(String(32), primary_key=True)
    memotext = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    last_editor = Column(String(32))
    edits = Column(Text)


class Note(Base):
    __tablename__ = 'notes'

    id = Column(INTEGER(11), primary_key=True)
    ckey = Column(String(32), nullable=False, index=True)
    notetext = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    round_id = Column(INTEGER(11))
    adminckey = Column(String(32), nullable=False)
    last_editor = Column(String(32))
    edits = Column(Text)
    server = Column(String(50), nullable=False)
    crew_playtime = Column(MEDIUMINT(8), server_default=text("0"))
    automated = Column(TINYINT(3), server_default=text("0"))


class OauthToken(Base):
    __tablename__ = 'oauth_tokens'

    ckey = Column(String(32), nullable=False, index=True)
    token = Column(String(32), primary_key=True)


class PaiSave(Base):
    __tablename__ = 'pai_saves'

    id = Column(INTEGER(11), primary_key=True)
    ckey = Column(String(50), nullable=False, unique=True)
    pai_name = Column(LONGTEXT)
    description = Column(LONGTEXT)
    preferred_role = Column(LONGTEXT)
    ooc_comments = Column(LONGTEXT)


class Player(Base):
    __tablename__ = 'player'

    id = Column(INTEGER(11), primary_key=True)
    ckey = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    firstseen = Column(DateTime, nullable=False)
    lastseen = Column(DateTime, nullable=False, index=True)
    ip = Column(String(18, 'utf8mb4_unicode_ci'), nullable=False, index=True)
    computerid = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, index=True)
    lastadminrank = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'Player'"))
    ooccolor = Column(String(7, 'utf8mb4_unicode_ci'), server_default=text("'#b82e00'"))
    UI_style = Column(String(10, 'utf8mb4_unicode_ci'), server_default=text("'Midnight'"))
    UI_style_color = Column(String(7, 'utf8mb4_unicode_ci'), server_default=text("'#ffffff'"))
    UI_style_alpha = Column(SMALLINT(4), server_default=text("255"))
    be_role = Column(LONGTEXT)
    default_slot = Column(SMALLINT(4), server_default=text("1"))
    toggles = Column(INTEGER(11))
    toggles_2 = Column(INTEGER(11))
    sound = Column(MEDIUMINT(8), server_default=text("31"))
    volume_mixer = Column(LONGTEXT)
    lastchangelog = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'0'"))
    exp = Column(LONGTEXT)
    clientfps = Column(SMALLINT(4), server_default=text("63"))
    atklog = Column(SMALLINT(4), server_default=text("0"))
    fuid = Column(BIGINT(20), index=True)
    fupdate = Column(SMALLINT(4), index=True, server_default=text("0"))
    parallax = Column(TINYINT(1), server_default=text("8"))
    byond_date = Column(Date)
    _2fa_status = Column('2fa_status', ENUM('DISABLED', 'ENABLED_IP', 'ENABLED_ALWAYS'), nullable=False, server_default=text("'DISABLED'"))
    screentip_mode = Column(TINYINT(1), server_default=text("8"))
    screentip_color = Column(String(7, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'#ffd391'"))
    ghost_darkness_level = Column(TINYINT(1), nullable=False, server_default=text("255"))
    colourblind_mode = Column(VARCHAR(48), nullable=False, server_default=text("'None'"))
    keybindings = Column(LONGTEXT)
    server_region = Column(VARCHAR(32))
    muted_adminsounds_ckeys = Column(MEDIUMTEXT)
    viewrange = Column(String(5, 'utf8mb4_unicode_ci'), nullable=False, server_default=text("'19x15'"))


class PlaytimeHistory(Base):
    __tablename__ = 'playtime_history'

    ckey = Column(String(32), primary_key=True, nullable=False)
    date = Column(Date, primary_key=True, nullable=False)
    time_living = Column(SMALLINT(6), nullable=False)
    time_ghost = Column(SMALLINT(6), nullable=False)


class Privacy(Base):
    __tablename__ = 'privacy'

    ckey = Column(String(32), primary_key=True)
    datetime = Column(DateTime, nullable=False)
    consent = Column(BIT(1), nullable=False)


class Round(Base):
    __tablename__ = 'round'

    id:Mapped[int] = mapped_column(primary_key=True)
    initialize_datetime = Column(DateTime, nullable=False)
    start_datetime = Column(DateTime)
    shutdown_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    server_ip = Column(INTEGER(10), nullable=False)
    server_port = Column(SMALLINT(5), nullable=False)
    commit_hash = Column(CHAR(40))
    game_mode = Column(String(32))
    game_mode_result = Column(String(64))
    end_state = Column(String(64))
    shuttle_name = Column(String(64))
    map_name = Column(String(32))
    station_name = Column(String(80))
    server_id = Column(String(50))

    feedbacks:Mapped[List["Feedback"]] = relationship(back_populates="round", innerjoin=True, lazy='joined')
    populations:Mapped[List["LegacyPopulation"]] = relationship(
        "LegacyPopulation",
        primaryjoin='and_(LegacyPopulation.time>=Round.initialize_datetime, LegacyPopulation.time<=Round.shutdown_datetime)',
        foreign_keys=[initialize_datetime, shutdown_datetime],
        viewonly=True,
        uselist=True,
    )

    def __repr__(self):
        return f"<Round#{self.id} [{self.start_datetime.strftime('%Y-%m-%d')}] {self.game_mode}/{self.map_name}>"

    @staticmethod
    def download(round_id):
        rq_session = make_cached_limiter_session()
        config = toml.load(open('config.toml'))
        connection_string = config['database']['prod_connection_string']
        engine = create_engine(connection_string)
        session = Session(engine)

        if session.get(Round, round_id):
            return

        print(f"getting round {round_id}")
        mtd = rq_session.get(f"{API_URL}/metadata/{round_id}").json()
        pct = rq_session.get(f"{API_URL}/playercounts/{round_id}").json()
        bbl = rq_session.get(f"{API_URL}/blackbox/{round_id}").json()

        with Session(engine, expire_on_commit=False) as t:
            rnd = Round(
                id=mtd["round_id"],
                initialize_datetime=mtd["init_datetime"],
                start_datetime=mtd["start_datetime"],
                shutdown_datetime=mtd["shutdown_datetime"],
                end_datetime=mtd["end_datetime"],
                commit_hash=mtd["commit_hash"],
                game_mode=mtd["game_mode"],
                game_mode_result=mtd["game_mode_result"],
                end_state=mtd["end_state"],
                map_name=mtd["map_name"],
                server_id=mtd["server_id"],

                server_ip=0,
                server_port=0,
            )                
            pcts = list()
            for dt, ct in pct.items():
                lp = LegacyPopulation(
                    playercount=ct,
                    admincount=0,
                    server_id=mtd["server_id"],
                    time=dt)
                pcts.append(lp)
            data = list()
            for row in bbl:
                fb = Feedback(
                    round_id=mtd["round_id"],
                    key_name=row["key_name"],
                    key_type=row["key_type"],
                    version=row["version"],
                    json=row["raw_data"],
                
                    datetime=mtd["init_datetime"])
                data.append(fb)

            t.add_all([rnd] + pcts + data)
            t.commit()

    def get_feedback_stat(self, k):
        for x in self.feedbacks:
            if x.key_name == k:
                return x

    def has_feedback_stat(self, name):
        for x in self.feedbacks:
            if x.key_name == name:
                return True
        return False

    def roundstart_ready_count(self, with_assts=False):
        if with_assts:
            return self.get_feedback_stat('job_preferences')['Nanotrasen Navy Officer']['never']

        return self.get_feedback_stat('job_preferences')['Assistant']['never']
    
    def has_testmerge(self, pr_id):
        if self.has_feedback_stat('testmerged_prs'):
            tprs = self.get_feedback_stat('testmerged_prs')
            for pr in tprs.values():
                if pr['number'] == str(pr_id):
                    return True
                
        return False

    @property
    def roundstart_client_count(self):
        return sorted(self.populations, key=lambda x:x.time)[0].playercount

    def roundstart_job_count(self, with_assts=False):
        if with_assts:
            return sum([y.get("roundstart", 0) for x,y in self.get_feedback_stat('manifest').items()])
        return sum([y.get("roundstart", 0) for x,y in self.get_feedback_stat('manifest').items() if x != 'Assistant'])

t_snapshot_data = Table(
    'snapshot_data', metadata,
    Column('snapshot_id', INTEGER(11), nullable=False),
    Column('id', Text, nullable=False),
    Column('path', Text, nullable=False),
    Column('x', INTEGER(8), nullable=False),
    Column('y', INTEGER(8), nullable=False),
    Column('z', INTEGER(8), nullable=False)
)


class Snapshot(Base):
    __tablename__ = 'snapshots'

    id = Column(INTEGER(11), primary_key=True)
    creator = Column(String(32), nullable=False)
    datetime = Column(DateTime, nullable=False)


class Ticket(Base):
    __tablename__ = 'tickets'
    __table_args__ = (
        CheckConstraint('json_valid(`all_responses`)'),
        CheckConstraint('json_valid(`awho`)')
    )

    id = Column(INTEGER(11), primary_key=True)
    ticket_num = Column(INTEGER(11), nullable=False)
    ticket_type = Column(Enum('ADMIN', 'MENTOR'), nullable=False)
    real_filetime = Column(DateTime, nullable=False)
    relative_filetime = Column(Time, nullable=False)
    ticket_creator = Column(String(32), nullable=False)
    ticket_topic = Column(Text, nullable=False)
    ticket_taker = Column(String(32))
    ticket_take_time = Column(DateTime)
    all_responses = Column(LONGTEXT)
    awho = Column(LONGTEXT, nullable=False)
    end_round_state = Column(Enum('OPEN', 'CLOSED', 'RESOLVED', 'STALE', 'UNKNOWN'), nullable=False)


class VpnWhitelist(Base):
    __tablename__ = 'vpn_whitelist'

    ckey = Column(String(32), primary_key=True)
    reason = Column(Text)


class Watch(Base):
    __tablename__ = 'watch'

    ckey = Column(String(32, 'utf8mb4_unicode_ci'), primary_key=True)
    reason = Column(MEDIUMTEXT, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    adminckey = Column(String(32, 'utf8mb4_unicode_ci'), nullable=False)
    last_editor = Column(String(32, 'utf8mb4_unicode_ci'))
    edits = Column(MEDIUMTEXT)