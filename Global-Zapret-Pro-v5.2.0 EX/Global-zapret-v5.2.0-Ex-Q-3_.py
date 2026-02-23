#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

import os
import sys
import json
import time
import threading
import subprocess
import ctypes
import atexit
import socket
import requests
import random
import struct
import re
from dataclasses import dataclass, asdict, field
from typing import Dict, Optional, List, Tuple, Set, Any
from enum import Enum
from pathlib import Path
from functools import lru_cache
from urllib.parse import urlparse
from datetime import datetime

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import pystray
from pystray import MenuItem as item

# ==============================================================================
# НЕОНОВАЯ ЦВЕТОВАЯ СХЕМА (КИБЕРПАНК)
# ==============================================================================

NEON_THEME = {
    "appearance": "dark",
    "color_theme": "blue",
    
    # Основные цвета
    "primary": "#00ffff",      # Циановый неон
    "secondary": "#ff00ff",     # Пурпурный неон
    "tertiary": "#ffff00",      # Желтый неон
    
    # Градиенты для кнопок
    "gradient_start": "#0066cc",
    "gradient_end": "#00ccff",
    
    # Состояния
    "success": "#00ff80",       # Мятный неон
    "error": "#ff3366",         # Розовый неон
    "warning": "#ffaa00",       # Оранжевый неон
    "info": "#00ccff",          # Голубой неон
    
    # Фоны
    "bg_primary": "#0a0a1a",    # Темно-синий
    "bg_secondary": "#1a1a2f",  # Сине-фиолетовый
    "bg_tertiary": "#2a2a3f",   # Фиолетовый
    
    # Текст
    "text_primary": "#ffffff",   # Белый
    "text_secondary": "#b0b0ff", # Светло-сиреневый
    "text_dim": "#606080",       # Приглушенный фиолетовый
    
    # Границы
    "border_primary": "#00ffff", # Циановый
    "border_secondary": "#ff00ff", # Пурпурный
    
    # Эффекты
    "glow": "#00ffff",           # Свечение
    "shadow": "#000080",         # Тень
}

# Размер окна (уменьшен на 10%)
WINDOW_WIDTH = 610  # было 680
WINDOW_HEIGHT = 740  # было 820

# Порты
TCP_PORTS = "80,88,443,1400,2053,2083,2087,2096,5222,5223,5228,8080,8443"
UDP_PORTS = "443,19294-19344,50000-50100"

# Сервисы
SERVICES_LIST = [
    "general", "google", "meta", "x", "tiktok", "telegram", "mylist", "games", "discord"
]

SERVICE_LISTS = {
    "general": "list-general.txt",
    "google": "list-google.txt",
    "meta": "list-meta.txt",
    "x": "list-x.txt",
    "tiktok": "list-tiktok.txt",
    "telegram": "list-telegram.txt",
    "mylist": "list-mylist.txt",
    "games": "list-games.txt",
    "discord": None
}

TLS_PATTERNS = {
    "google": "tls_clienthello_www_google_com.bin",
    "meta": "tls_clienthello_4pda_to.bin",
    "x": "tls_clienthello_max_ru.bin",
    "tiktok": "tls_clienthello_max_ru.bin",
    "telegram": "tls_clienthello_max_ru.bin",
    "mylist": "tls_clienthello_max_ru.bin",
    "games": "tls_clienthello_max_ru.bin",
    "general": "tls_clienthello_max_ru.bin"
}

# ==============================================================================
# РЕЖИМЫ РАБОТЫ
# ==============================================================================

class Mode(Enum):
    LITE = "ЛАЙТ"
    STANDARD = "СТАНДАРТ"
    AGGRESSIVE = "АГРЕССИВ"
    ULTRA = "УЛЬТРА"
    PERFORMANCE = "ПРОИЗВ."
    UNIVERSAL = "УНИВЕРС."
    GAMING = "ИГРОВОЙ"
    STEALTH = "СТЕЛС"
    EXTREME = "ЭКСТРИМ"
    RANDOM = "РАНДОМ"
    MULTI = "МУЛЬТИ"


class BlockType(Enum):
    DNS = "DNS"
    IP = "IP"
    TCP = "TCP"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    DPI = "DPI"
    SNI = "SNI"
    TLS = "TLS"
    QUIC = "QUIC"
    RST = "RST"
    TIMEOUT = "TIMEOUT"
    UNKNOWN = "UNKNOWN"


class BypassMethod(Enum):
    FAKE = "fake"
    FAKE2 = "fake2"
    FAKE_MULTI = "fake_multi"
    MULTISPLIT = "multisplit"
    MULTISPLIT2 = "multisplit2"
    SPLIT = "split"
    SPLIT2 = "split2"
    SPLIT3 = "split3"
    SPLIT4 = "split4"
    SPLIT5 = "split5"
    DISORDER = "disorder"
    DISORDER2 = "disorder2"
    DISORDER3 = "disorder3"
    DISORDER4 = "disorder4"
    DISORDER5 = "disorder5"
    OOO = "ooo"
    OOO2 = "ooo2"
    REORDER = "reorder"
    REORDER2 = "reorder2"
    FRAGMENT = "fragment"
    FRAGMENT2 = "fragment2"
    FRAGMENT3 = "fragment3"
    FRAGMENT4 = "fragment4"
    FRAGMENT5 = "fragment5"
    FRAGMENT6 = "fragment6"
    FRAGMENT7 = "fragment7"
    FRAGMENT8 = "fragment8"
    MFRAG = "mfrag"
    MFRAG2 = "mfrag2"
    MFRAG3 = "mfrag3"
    BADSUM = "badsum"
    BADSUM2 = "badsum2"
    BADSUM3 = "badsum3"
    MD5 = "md5"
    MD5SIG = "md5sig"
    MD5SIG2 = "md5sig2"
    MD5SIG3 = "md5sig3"
    CRC = "crc"
    CRC2 = "crc2"
    CRC3 = "crc3"
    CHECKSUM = "checksum"
    CHECKSUM2 = "checksum2"
    HOLE = "hole"
    HOLE2 = "hole2"
    HOLE3 = "hole3"
    HOLE4 = "hole4"
    HOLE5 = "hole5"
    HOLE_PACKET = "hole_packet"
    HOLE_STREAM = "hole_stream"
    SEQOVL = "seqovl"
    SEQOVL2 = "seqovl2"
    SEQOVL3 = "seqovl3"
    SEQOVL4 = "seqovl4"
    SEQOVL5 = "seqovl5"
    SEQOVL6 = "seqovl6"
    SEQOVL7 = "seqovl7"
    SEQOVL8 = "seqovl8"
    SEQOVL9 = "seqovl9"
    SEQOVL10 = "seqovl10"
    TCPOPT = "tcpopt"
    TCPOPT2 = "tcpopt2"
    TCPOPT3 = "tcpopt3"
    TCPOPT4 = "tcpopt4"
    WSIZE = "wsize"
    WSIZE2 = "wsize2"
    WSIZE3 = "wsize3"
    WSIZE4 = "wsize4"
    WSIZE5 = "wsize5"
    MSS = "mss"
    MSS2 = "mss2"
    MSS3 = "mss3"
    TTL = "ttl"
    TTL2 = "ttl2"
    TTL3 = "ttl3"
    TTL4 = "ttl4"
    TTL_RANDOM = "ttl_random"
    TTL_DEC = "ttl_dec"
    TTL_INC = "ttl_inc"
    PADDING = "padding"
    PADDING2 = "padding2"
    PADDING3 = "padding3"
    PADDING4 = "padding4"
    PADDING5 = "padding5"
    PADDING_RANDOM = "padding_random"
    PADDING_TCP = "padding_tcp"
    PADDING_UDP = "padding_udp"
    ENCRYPT = "encrypt"
    ENCRYPT2 = "encrypt2"
    ENCRYPT3 = "encrypt3"
    MIMIC = "mimic"
    MIMIC2 = "mimic2"
    MIMIC3 = "mimic3"
    MIMIC_HTTP = "mimic_http"
    MIMIC_HTTPS = "mimic_https"
    MIMIC_DNS = "mimic_dns"
    MIMIC_QUIC = "mimic_quic"
    TUNNEL = "tunnel"
    TUNNEL2 = "tunnel2"
    TUNNEL3 = "tunnel3"
    PROXY = "proxy"
    PROXY_HTTP = "proxy_http"
    PROXY_SOCKS4 = "proxy_socks4"
    PROXY_SOCKS5 = "proxy_socks5"
    PROXY_SSL = "proxy_ssl"
    HEARTBLEED = "heartbleed"
    HEARTBLEED2 = "heartbleed2"
    BLEED = "bleed"
    BLEED2 = "bleed2"
    TLS_SPLIT = "tls_split"
    TLS_SPLIT2 = "tls_split2"
    TLS_SPLIT3 = "tls_split3"
    QUIC_SPLIT = "quic_split"
    QUIC_SPLIT2 = "quic_split2"
    QUIC_SPLIT3 = "quic_split3"
    RANDOM = "random"
    RANDOM2 = "random2"
    RANDOM3 = "random3"
    RANDOM_SPLIT = "random_split"
    RANDOM_SPLIT2 = "random_split2"
    RANDOM_SPLIT3 = "random_split3"
    RANDOM_HOLE = "random_hole"
    RANDOM_FRAG = "random_frag"
    MULTI_FAKE = "multi_fake"
    MULTI_FAKE2 = "multi_fake2"
    MULTI_FAKE3 = "multi_fake3"
    MULTI_SPLIT = "multi_split"
    MULTI_HOLE = "multi_hole"
    MULTI_FRAG = "multi_frag"
    MULTI_ALL = "multi_all"
    AUTO = "auto"
    AUTO2 = "auto2"
    AUTO3 = "auto3"
    SMART = "smart"
    SMART2 = "smart2"
    SMART3 = "smart3"
    TLS12 = "tls12"
    TLS13 = "tls13"
    TLS_OLD = "tls_old"
    TLS_NEW = "tls_new"
    QUIC = "quic"
    QUIC_OLD = "quic_old"
    QUIC_NEW = "quic_new"
    HTTP = "http"
    HTTP2 = "http2"
    HTTP3 = "http3"
    HTTPS = "https"
    WEBSOCKET = "websocket"
    WEBSOCKET2 = "websocket2"
    WEBSOCKET3 = "websocket3"
    DNS = "dns"
    DNS2 = "dns2"
    DNS3 = "dns3"
    FAKE_MULTISPLIT = "fake,multisplit"
    FAKE_MULTISPLIT_DISORDER = "fake,multisplit,disorder"
    FAKE_MULTISPLIT_DISORDER2 = "fake,multisplit,disorder2"
    FAKE_MULTISPLIT_DISORDER3 = "fake,multisplit,disorder3"
    FAKE_MULTISPLIT_HOLE = "fake,multisplit,hole"
    FAKE_MULTISPLIT_HOLE2 = "fake,multisplit,hole2"
    FAKE_MULTISPLIT_FRAG = "fake,multisplit,fragment"
    FAKE_MULTISPLIT_FRAG2 = "fake,multisplit,fragment2"
    FAKE_MULTISPLIT_BADSUM = "fake,multisplit,badsum"
    FAKE_MULTISPLIT_MD5 = "fake,multisplit,md5sig"
    FAKE_HOLE = "fake,hole"
    FAKE_HOLE2 = "fake,hole2"
    FAKE_FRAG = "fake,fragment"
    FAKE_FRAG2 = "fake,fragment2"
    FAKE_BADSUM = "fake,badsum"
    FAKE_MD5 = "fake,md5sig"
    MULTISPLIT_HOLE = "multisplit,hole"
    MULTISPLIT_HOLE2 = "multisplit,hole2"
    MULTISPLIT_FRAG = "multisplit,fragment"
    MULTISPLIT_FRAG2 = "multisplit,fragment2"
    MULTISPLIT_BADSUM = "multisplit,badsum"
    DISORDER_HOLE = "disorder,hole"
    DISORDER2_HOLE = "disorder2,hole"
    DISORDER3_HOLE = "disorder3,hole"
    FRAG_HOLE = "fragment,hole"
    FRAG2_HOLE = "fragment2,hole"
    FRAG3_HOLE = "fragment3,hole"
    ALL_BASIC = "fake,multisplit,split,disorder"
    ALL_ADVANCED = "fake,multisplit,disorder2,hole,fragment,badsum"
    ALL_EXTREME = "fake,multisplit,disorder3,hole2,fragment2,badsum2,md5sig"
    ALL_ULTIMATE = "fake,multisplit,disorder4,hole3,fragment3,badsum3,md5sig2,seqovl"
    ALL_MAX = "fake,multisplit,disorder5,hole4,fragment4,badsum3,md5sig3,seqovl2,tcpopt"
    ALL_INSANE = "fake,multisplit,disorder5,hole5,fragment5,badsum3,md5sig3,seqovl3,tcpopt2,wsize3"
    ALL_GOD = "fake,multisplit,disorder5,hole5,fragment8,badsum3,md5sig3,seqovl4,tcpopt3,wsize4,mfrag3"
    ADVANCED1 = "fake,multisplit,disorder2,hole,fragment2"
    ADVANCED2 = "fake,multisplit,disorder3,hole2,fragment3"
    ADVANCED3 = "fake,multisplit,disorder4,hole3,fragment4"
    ADVANCED4 = "fake,multisplit,disorder5,hole4,fragment5"
    ADVANCED5 = "fake,multisplit,disorder5,hole5,fragment6"
    ADVANCED6 = "fake,multisplit,disorder5,hole5,fragment7"
    ADVANCED7 = "fake,multisplit,disorder5,hole5,fragment8"
    ADVANCED8 = "fake,multisplit,disorder5,hole5,mfrag"
    ADVANCED9 = "fake,multisplit,disorder5,hole5,mfrag2"
    ADVANCED10 = "fake,multisplit,disorder5,hole5,mfrag3"
    STEALTH1 = "hole,badsum"
    STEALTH2 = "hole2,badsum2"
    STEALTH3 = "hole3,badsum3"
    STEALTH4 = "hole4,md5sig"
    STEALTH5 = "hole5,md5sig2"
    STEALTH6 = "hole5,md5sig3"
    STEALTH7 = "hole5,badsum3,md5sig3"
    STEALTH8 = "hole5,fragment,badsum"
    STEALTH9 = "hole5,fragment2,badsum2"
    STEALTH10 = "hole5,fragment3,badsum3"
    GAMING1 = "split2"
    GAMING2 = "split2,disorder"
    GAMING3 = "split2,disorder2"
    GAMING4 = "split2,fragment"
    GAMING5 = "split2,fragment2"
    GAMING6 = "split2,hole"
    GAMING7 = "split2,hole2"
    GAMING8 = "split2,badsum"
    GAMING9 = "split2,md5sig"
    GAMING10 = "split2,disorder2,fragment2"
    YOUTUBE = "fake,multisplit,disorder2"
    YOUTUBE2 = "fake,multisplit,disorder2,hole"
    YOUTUBE3 = "fake,multisplit,disorder2,hole,fragment"
    NETFLIX = "fake,multisplit,hole"
    NETFLIX2 = "fake,multisplit,hole2"
    NETFLIX3 = "fake,multisplit,hole3"
    TWITCH = "fake,multisplit,disorder,fragment"
    TWITCH2 = "fake,multisplit,disorder2,fragment2"
    TWITCH3 = "fake,multisplit,disorder3,fragment3"
    DISCORD = "fake,fakedsplit"
    DISCORD2 = "fake,fakedsplit,hole"
    DISCORD3 = "fake,fakedsplit,hole2"
    TELEGRAM = "fake,multisplit"
    TELEGRAM2 = "fake,multisplit,hole"
    TELEGRAM3 = "fake,multisplit,hole,fragment"
    EXPERIMENTAL1 = "experimental"
    EXPERIMENTAL2 = "experimental2"
    EXPERIMENTAL3 = "experimental3"
    EXPERIMENTAL4 = "experimental4"
    EXPERIMENTAL5 = "experimental5"
    BETA1 = "beta"
    BETA2 = "beta2"
    BETA3 = "beta3"
    ALPHA1 = "alpha"
    ALPHA2 = "alpha2"
    ALPHA3 = "alpha3"
    TEST1 = "test"
    TEST2 = "test2"
    TEST3 = "test3"
    TEST4 = "test4"
    TEST5 = "test5"
    DEBUG1 = "debug"
    DEBUG2 = "debug2"
    DEBUG3 = "debug3"


# ==============================================================================
# DATACLASSES
# ==============================================================================

@dataclass
class DPIProfile:
    repeats: str
    split_pos: int = 1
    fooling: str = "ts"
    desync: str = "--dpi-desync=fake,multisplit"
    methods: List[str] = field(default_factory=list)
    
    @classmethod
    def get_default_profiles(cls) -> Dict[Mode, 'DPIProfile']:
        return {
            Mode.LITE: cls(
                repeats="--dpi-desync-repeats=4",
                split_pos=1,
                fooling="ts",
                desync="--dpi-desync=fake",
                methods=["fake"]
            ),
            Mode.STANDARD: cls(
                repeats="--dpi-desync-repeats=6",
                split_pos=1,
                fooling="ts",
                desync="--dpi-desync=fake,multisplit",
                methods=["fake", "multisplit"]
            ),
            Mode.AGGRESSIVE: cls(
                repeats="--dpi-desync-repeats=10",
                split_pos=2,
                fooling="md5sig",
                desync="--dpi-desync=fake,multisplit,disorder2",
                methods=["fake", "multisplit", "disorder2"]
            ),
            Mode.ULTRA: cls(
                repeats="--dpi-desync-repeats=12",
                split_pos=3,
                fooling="md5",
                desync="--dpi-desync=fake,multisplit,disorder2,hole",
                methods=["fake", "multisplit", "disorder2", "hole"]
            ),
            Mode.PERFORMANCE: cls(
                repeats="--dpi-desync-repeats=4",
                split_pos=1,
                fooling="ts",
                desync="--dpi-desync=fake",
                methods=["fake"]
            ),
            Mode.UNIVERSAL: cls(
                repeats="--dpi-desync-repeats=8",
                split_pos=2,
                fooling="ts",
                desync="--dpi-desync=fake,multisplit,split2",
                methods=["fake", "multisplit", "split2"]
            ),
            Mode.GAMING: cls(
                repeats="--dpi-desync-repeats=6",
                split_pos=1,
                fooling="ts",
                desync="--dpi-desync=split2",
                methods=["split2"]
            ),
            Mode.STEALTH: cls(
                repeats="--dpi-desync-repeats=8",
                split_pos=4,
                fooling="badsum",
                desync="--dpi-desync=fake,hole,badsum",
                methods=["fake", "hole", "badsum"]
            ),
            Mode.EXTREME: cls(
                repeats="--dpi-desync-repeats=15",
                split_pos=5,
                fooling="md5sig,badsum",
                desync="--dpi-desync=fake,multisplit,disorder2,hole,fragment,badsum",
                methods=["fake", "multisplit", "disorder2", "hole", "fragment", "badsum"]
            ),
            Mode.RANDOM: cls(
                repeats="--dpi-desync-repeats=10",
                split_pos=3,
                fooling="random",
                desync="--dpi-desync=random_split,multi_fake",
                methods=["random_split", "multi_fake"]
            ),
            Mode.MULTI: cls(
                repeats="--dpi-desync-repeats=12",
                split_pos=4,
                fooling="md5sig",
                desync="--dpi-desync=fake,multisplit,disorder2,hole,fragment2,tls_split,quic_split",
                methods=["fake", "multisplit", "disorder2", "hole", "fragment2", "tls_split", "quic_split"]
            )
        }


@dataclass
class PacketConfig:
    tcp_ports: str = TCP_PORTS
    udp_ports: str = UDP_PORTS
    game_filter: str = ""
    split_pos: int = 1
    fooling: str = "ts"
    auto_restart: bool = True
    fragment_size: int = 128
    ttl_min: int = 32
    ttl_max: int = 128
    window_size: int = 65535
    randomize: bool = False
    use_proxy: bool = False
    proxy_address: str = "socks5://127.0.0.1:1080"
    custom_methods: str = ""


@dataclass
class ServiceConfig:
    enabled: bool = True
    tcp_ports: str = TCP_PORTS
    udp_ports: str = ""
    repeats: str = "--dpi-desync-repeats=8"
    desync: str = "--dpi-desync=fake,multisplit"
    tls_bin: str = "tls_clienthello_max_ru.bin"
    quic_bin: str = "quic_initial_www_google_com.bin"
    split_pos: int = 1
    fooling: str = "ts"
    use_quic: bool = True
    is_discord: bool = False
    is_general: bool = False


# ==============================================================================
# БАЗОВЫЙ КЛАСС ДЛЯ НЕОНОВЫХ ОКОН
# ==============================================================================

class NeonBaseWindow:
    """Базовый класс для всех окон в неоновом стиле"""
    
    def __init__(self, window):
        self.window = window
        self._setup_neon_style()
        self._setup_icon()
    
    def _setup_neon_style(self):
        """Настройка неонового стиля"""
        self.window.configure(fg_color=NEON_THEME['bg_primary'])
        
        # Устанавливаем прозрачность для эффекта свечения
        try:
            self.window.attributes('-alpha', 0.98)
        except:
            pass
    
    def _setup_icon(self):
        """Установка иконки - ТОЛЬКО BLUE.ICO"""
        try:
            icon_path = self._get_icon_path()
            if os.path.exists(icon_path):
                self.window.after(200, lambda: self._set_icon(icon_path))
        except:
            pass
    
    def _get_icon_path(self) -> str:
        """Получение пути к иконке - ТОЛЬКО BLUE.ICO"""
        config = ConfigManager()
        if getattr(sys, 'frozen', False):
            path = os.path.join(sys._MEIPASS, "BLUE.ico")
            if os.path.exists(path):
                return path
        return os.path.join(config.base_path, "BLUE.ico")
    
    def _set_icon(self, icon_path: str):
        try:
            self.window.iconbitmap(icon_path)
        except:
            pass
    
    @staticmethod
    def _get_resource_path(relative_path: str) -> str:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)
    
    def _create_neon_header(self, parent, title_text: str, subtitle_text: str = ""):
        """Создание неонового заголовка"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent", height=80)
        header_frame.pack(pady=(15, 10), fill="x")
        header_frame.pack_propagate(False)
        
        # Верхняя линия с неоновым свечением
        top_line = ctk.CTkFrame(header_frame, height=2, fg_color=NEON_THEME['primary'])
        top_line.pack(fill="x", padx=25, pady=(0, 8))
        
        # Основной заголовок с градиентным эффектом
        title = ctk.CTkLabel(
            header_frame,
            text=title_text,
            font=("Courier New", 24, "bold"),
            text_color=NEON_THEME['primary']
        )
        title.pack()
        
        # Дополнительный текст с неоновым эффектом
        if subtitle_text:
            subtitle = ctk.CTkLabel(
                header_frame,
                text=subtitle_text,
                font=("Courier New", 10),
                text_color=NEON_THEME['secondary']
            )
            subtitle.pack(pady=(4, 0))
        
        # Нижняя линия
        bottom_line = ctk.CTkFrame(header_frame, height=1, fg_color=NEON_THEME['secondary'])
        bottom_line.pack(fill="x", padx=45, pady=(8, 0))


# ==============================================================================
# МЕНЕДЖЕРЫ
# ==============================================================================

class ConfigManager:
    CONFIG_FILE = "config.json"
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.base_path = self._get_base_path()
        self.config_path = Path(self.base_path) / self.CONFIG_FILE
        self.cache = {}
        self.cache_lock = threading.Lock()
        self._default_config = self._create_default_config()
        self.data = self.load()
    
    @staticmethod
    def _get_base_path() -> str:
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))
    
    @staticmethod
    def _get_resource_path(relative_path: str) -> str:
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, relative_path)
    
    def _create_default_config(self) -> dict:
        return {
            "mode": "УНИВЕРС.",
            "services": {
                "general": {"enabled": True},
                "google": {"enabled": True},
                "meta": {"enabled": True},
                "x": {"enabled": True},
                "tiktok": {"enabled": True},
                "telegram": {"enabled": True},
                "mylist": {"enabled": True},
                "games": {"enabled": True},
                "discord": {"enabled": True}
            },
            "packets": {
                "tcp_ports": TCP_PORTS,
                "udp_ports": UDP_PORTS,
                "split_pos": 1,
                "fooling": "ts",
                "auto_restart": True,
                "fragment_size": 128,
                "ttl_min": 32,
                "ttl_max": 128,
                "window_size": 65535,
                "randomize": False,
                "use_proxy": False,
                "proxy_address": "socks5://127.0.0.1:1080",
                "custom_methods": "fake,multisplit,disorder2,hole,fragment,badsum"
            },
            "autostart": False,
            "auto_run": True,
            "start_minimized": True,
            "show_notifications": True,
            "first_start": True
        }
    
    def load(self) -> dict:
        with self.cache_lock:
            if 'config' in self.cache:
                return self.cache['config'].copy()
            
            config = self._default_config.copy()
            
            try:
                if self.config_path.exists():
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        loaded = json.load(f)
                        self._deep_update(config, loaded)
            except Exception as e:
                print(f"[!] Ошибка загрузки: {e}")
            
            self.cache['config'] = config.copy()
            return config.copy()
    
    def _deep_update(self, target: dict, source: dict):
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_update(target[key], value)
            else:
                target[key] = value
    
    def save(self):
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
            with self.cache_lock:
                self.cache['config'] = self.data.copy()
        except Exception as e:
            print(f"[!] Ошибка сохранения: {e}")
    
    def get(self, key: str, default=None):
        keys = key.split('.')
        value = self.data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        keys = key.split('.')
        target = self.data
        
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        target[keys[-1]] = value
        self.save()


class ListsManager:
    REQUIRED_LISTS = {
        'ipset-exclude.txt',
        'list-exclude.txt',
        'list-games.txt',
        'list-general.txt',
        'list-google.txt',
        'list-ip.txt',
        'list-meta.txt',
        'list-mylist.txt',
        'list-telegram.txt',
        'list-tiktok.txt',
        'list-x.txt',
        'ipset-all.txt'
    }
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.lists_path = os.path.join(base_path, "lists")
        self.available_lists: Set[str] = set()
        self.list_cache: Dict[str, List[str]] = {}
        self.cache_lock = threading.Lock()
        self.scan_lists()
    
    def scan_lists(self) -> Set[str]:
        self.available_lists.clear()
        
        try:
            if not os.path.exists(self.lists_path):
                os.makedirs(self.lists_path, exist_ok=True)
                for list_name in self.REQUIRED_LISTS:
                    filepath = os.path.join(self.lists_path, list_name)
                    if not os.path.exists(filepath):
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write("# НЕОНОВЫЙ СПИСОК\n")
                return self.available_lists
            
            for filename in os.listdir(self.lists_path):
                filepath = os.path.join(self.lists_path, filename)
                if os.path.isfile(filepath) and filename.endswith('.txt'):
                    self.available_lists.add(filename)
                    
        except Exception as e:
            print(f"[!] Ошибка сканирования: {e}")
        
        return self.available_lists.copy()
    
    @lru_cache(maxsize=32)
    def get_list_path(self, list_name: str) -> Optional[str]:
        filepath = os.path.join(self.lists_path, list_name)
        return filepath if os.path.exists(filepath) else None
    
    def check_list_exists(self, list_name: str) -> bool:
        return self.get_list_path(list_name) is not None
    
    def read_list(self, list_name: str) -> List[str]:
        with self.cache_lock:
            if list_name in self.list_cache:
                return self.list_cache[list_name].copy()
            
            filepath = self.get_list_path(list_name)
            if not filepath:
                return []
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = [line.strip() for line in f.readlines()]
                    content = [line for line in content if line and not line.startswith('#')]
                    self.list_cache[list_name] = content
                    return content.copy()
            except Exception as e:
                print(f"[!] Ошибка чтения {list_name}: {e}")
                return []
    
    def get_all_available_lists(self) -> Dict[str, List[str]]:
        result = {}
        for list_name in self.available_lists:
            result[list_name] = self.read_list(list_name)
        return result
    
    def clear_cache(self):
        with self.cache_lock:
            self.list_cache.clear()
            self.get_list_path.cache_clear()


class BypassMethodManager:
    def __init__(self):
        self.method_descriptions = {}
        self._init_descriptions()
    
    def _init_descriptions(self):
        desc = {
            BypassMethod.FAKE: "[БАЗОВЫЙ] fake - базовая подмена",
            BypassMethod.FAKE2: "[БАЗОВЫЙ] fake2 - усиленная подмена",
            BypassMethod.FAKE_MULTI: "[БАЗОВЫЙ] fake_multi - множественная подмена",
            BypassMethod.MULTISPLIT: "[РАЗДЕЛЕНИЕ] multisplit - множественное разделение",
            BypassMethod.MULTISPLIT2: "[РАЗДЕЛЕНИЕ] multisplit2 - усиленное разделение",
            BypassMethod.SPLIT: "[РАЗДЕЛЕНИЕ] split - простое разделение",
            BypassMethod.SPLIT2: "[РАЗДЕЛЕНИЕ] split2 - двойное разделение",
            BypassMethod.SPLIT3: "[РАЗДЕЛЕНИЕ] split3 - тройное разделение",
            BypassMethod.SPLIT4: "[РАЗДЕЛЕНИЕ] split4 - четверное разделение",
            BypassMethod.SPLIT5: "[РАЗДЕЛЕНИЕ] split5 - пятерное разделение",
            BypassMethod.DISORDER: "[ПОРЯДОК] disorder - нарушение порядка",
            BypassMethod.DISORDER2: "[ПОРЯДОК] disorder2 - усиленное нарушение",
            BypassMethod.DISORDER3: "[ПОРЯДОК] disorder3 - максимальное нарушение",
            BypassMethod.DISORDER4: "[ПОРЯДОК] disorder4 - экстремальное нарушение",
            BypassMethod.DISORDER5: "[ПОРЯДОК] disorder5 - полный хаос",
            BypassMethod.OOO: "[ПОРЯДОК] ooo - out-of-order",
            BypassMethod.OOO2: "[ПОРЯДОК] ooo2 - усиленный ooo",
            BypassMethod.REORDER: "[ПОРЯДОК] reorder - переупорядочивание",
            BypassMethod.REORDER2: "[ПОРЯДОК] reorder2 - двойное переупорядочивание",
            BypassMethod.FRAGMENT: "[ФРАГМЕНТАЦИЯ] fragment - фрагментация",
            BypassMethod.FRAGMENT2: "[ФРАГМЕНТАЦИЯ] fragment2 - усиленная фрагментация",
            BypassMethod.FRAGMENT3: "[ФРАГМЕНТАЦИЯ] fragment3 - максимальная",
            BypassMethod.FRAGMENT4: "[ФРАГМЕНТАЦИЯ] fragment4 - экстремальная",
            BypassMethod.FRAGMENT5: "[ФРАГМЕНТАЦИЯ] fragment5 - полная",
            BypassMethod.FRAGMENT6: "[ФРАГМЕНТАЦИЯ] fragment6 - мелкая",
            BypassMethod.FRAGMENT7: "[ФРАГМЕНТАЦИЯ] fragment7 - очень мелкая",
            BypassMethod.FRAGMENT8: "[ФРАГМЕНТАЦИЯ] fragment8 - крошечная",
            BypassMethod.MFRAG: "[ФРАГМЕНТАЦИЯ] mfrag - множественная",
            BypassMethod.MFRAG2: "[ФРАГМЕНТАЦИЯ] mfrag2 - усиленная множественная",
            BypassMethod.MFRAG3: "[ФРАГМЕНТАЦИЯ] mfrag3 - тройная множественная",
            BypassMethod.BADSUM: "[КОНТРОЛЬ] badsum - неправильная сумма",
            BypassMethod.BADSUM2: "[КОНТРОЛЬ] badsum2 - двойная неправильная",
            BypassMethod.BADSUM3: "[КОНТРОЛЬ] badsum3 - тройная неправильная",
            BypassMethod.MD5: "[КОНТРОЛЬ] md5 - md5 обфускация",
            BypassMethod.MD5SIG: "[КОНТРОЛЬ] md5sig - подмена md5",
            BypassMethod.MD5SIG2: "[КОНТРОЛЬ] md5sig2 - усиленная подмена",
            BypassMethod.MD5SIG3: "[КОНТРОЛЬ] md5sig3 - максимальная подмена",
            BypassMethod.CRC: "[КОНТРОЛЬ] crc - подмена crc",
            BypassMethod.CRC2: "[КОНТРОЛЬ] crc2 - двойная подмена",
            BypassMethod.CRC3: "[КОНТРОЛЬ] crc3 - тройная подмена",
            BypassMethod.CHECKSUM: "[КОНТРОЛЬ] checksum - подмена контрольной суммы",
            BypassMethod.CHECKSUM2: "[КОНТРОЛЬ] checksum2 - усиленная подмена",
            BypassMethod.HOLE: "[ДЫРЫ] hole - создание дыр",
            BypassMethod.HOLE2: "[ДЫРЫ] hole2 - усиленные дыры",
            BypassMethod.HOLE3: "[ДЫРЫ] hole3 - максимальные дыры",
            BypassMethod.HOLE4: "[ДЫРЫ] hole4 - экстремальные дыры",
            BypassMethod.HOLE5: "[ДЫРЫ] hole5 - полные дыры",
            BypassMethod.HOLE_PACKET: "[ДЫРЫ] hole_packet - дыры в пакетах",
            BypassMethod.HOLE_STREAM: "[ДЫРЫ] hole_stream - дыры в потоке",
            BypassMethod.SEQOVL: "[ПЕРЕКРЫТИЕ] seqovl - перекрытие",
            BypassMethod.SEQOVL2: "[ПЕРЕКРЫТИЕ] seqovl2 - двойное",
            BypassMethod.SEQOVL3: "[ПЕРЕКРЫТИЕ] seqovl3 - тройное",
            BypassMethod.SEQOVL4: "[ПЕРЕКРЫТИЕ] seqovl4 - четверное",
            BypassMethod.SEQOVL5: "[ПЕРЕКРЫТИЕ] seqovl5 - пятерное",
            BypassMethod.SEQOVL6: "[ПЕРЕКРЫТИЕ] seqovl6 - шестерное",
            BypassMethod.SEQOVL7: "[ПЕРЕКРЫТИЕ] seqovl7 - семерное",
            BypassMethod.SEQOVL8: "[ПЕРЕКРЫТИЕ] seqovl8 - восьмерное",
            BypassMethod.SEQOVL9: "[ПЕРЕКРЫТИЕ] seqovl9 - девятерное",
            BypassMethod.SEQOVL10: "[ПЕРЕКРЫТИЕ] seqovl10 - десятерное",
            BypassMethod.TCPOPT: "[TCP] tcpopt - модификация tcp опций",
            BypassMethod.TCPOPT2: "[TCP] tcpopt2 - усиленная",
            BypassMethod.TCPOPT3: "[TCP] tcpopt3 - максимальная",
            BypassMethod.TCPOPT4: "[TCP] tcpopt4 - экстремальная",
            BypassMethod.WSIZE: "[TCP] wsize - изменение окна",
            BypassMethod.WSIZE2: "[TCP] wsize2 - двойное",
            BypassMethod.WSIZE3: "[TCP] wsize3 - тройное",
            BypassMethod.WSIZE4: "[TCP] wsize4 - четверное",
            BypassMethod.WSIZE5: "[TCP] wsize5 - пятерное",
            BypassMethod.MSS: "[TCP] mss - изменение mss",
            BypassMethod.MSS2: "[TCP] mss2 - двойное",
            BypassMethod.MSS3: "[TCP] mss3 - тройное",
            BypassMethod.TTL: "[TTL] ttl - изменение ttl",
            BypassMethod.TTL2: "[TTL] ttl2 - двойное",
            BypassMethod.TTL3: "[TTL] ttl3 - тройное",
            BypassMethod.TTL4: "[TTL] ttl4 - четверное",
            BypassMethod.TTL_RANDOM: "[TTL] ttl_random - случайный ttl",
            BypassMethod.TTL_DEC: "[TTL] ttl_dec - уменьшение ttl",
            BypassMethod.TTL_INC: "[TTL] ttl_inc - увеличение ttl",
            BypassMethod.PADDING: "[PADDING] padding - добавление padding",
            BypassMethod.PADDING2: "[PADDING] padding2 - усиленное",
            BypassMethod.PADDING3: "[PADDING] padding3 - максимальное",
            BypassMethod.PADDING4: "[PADDING] padding4 - экстремальное",
            BypassMethod.PADDING5: "[PADDING] padding5 - полное",
            BypassMethod.PADDING_RANDOM: "[PADDING] padding_random - случайный",
            BypassMethod.PADDING_TCP: "[PADDING] padding_tcp - tcp padding",
            BypassMethod.PADDING_UDP: "[PADDING] padding_udp - udp padding",
            BypassMethod.ENCRYPT: "[ШИФРОВАНИЕ] encrypt - шифрование",
            BypassMethod.ENCRYPT2: "[ШИФРОВАНИЕ] encrypt2 - усиленное",
            BypassMethod.ENCRYPT3: "[ШИФРОВАНИЕ] encrypt3 - максимальное",
            BypassMethod.MIMIC: "[ИМИТАЦИЯ] mimic - имитация трафика",
            BypassMethod.MIMIC2: "[ИМИТАЦИЯ] mimic2 - усиленная",
            BypassMethod.MIMIC3: "[ИМИТАЦИЯ] mimic3 - максимальная",
            BypassMethod.MIMIC_HTTP: "[ИМИТАЦИЯ] mimic_http - имитация http",
            BypassMethod.MIMIC_HTTPS: "[ИМИТАЦИЯ] mimic_https - имитация https",
            BypassMethod.MIMIC_DNS: "[ИМИТАЦИЯ] mimic_dns - имитация dns",
            BypassMethod.MIMIC_QUIC: "[ИМИТАЦИЯ] mimic_quic - имитация quic",
            BypassMethod.TUNNEL: "[ТУННЕЛЬ] tunnel - туннелирование",
            BypassMethod.TUNNEL2: "[ТУННЕЛЬ] tunnel2 - усиленное",
            BypassMethod.TUNNEL3: "[ТУННЕЛЬ] tunnel3 - максимальное",
            BypassMethod.PROXY: "[ПРОКСИ] proxy - проксирование",
            BypassMethod.PROXY_HTTP: "[ПРОКСИ] proxy_http - http прокси",
            BypassMethod.PROXY_SOCKS4: "[ПРОКСИ] proxy_socks4 - socks4",
            BypassMethod.PROXY_SOCKS5: "[ПРОКСИ] proxy_socks5 - socks5",
            BypassMethod.PROXY_SSL: "[ПРОКСИ] proxy_ssl - ssl прокси",
            BypassMethod.HEARTBLEED: "[ЭКСПЛОЙТ] heartbleed - heartbleed",
            BypassMethod.HEARTBLEED2: "[ЭКСПЛОЙТ] heartbleed2 - усиленный",
            BypassMethod.BLEED: "[ЭКСПЛОЙТ] bleed - bleed метод",
            BypassMethod.BLEED2: "[ЭКСПЛОЙТ] bleed2 - усиленный bleed",
            BypassMethod.TLS_SPLIT: "[TLS] tls_split - tls разделение",
            BypassMethod.TLS_SPLIT2: "[TLS] tls_split2 - двойное",
            BypassMethod.TLS_SPLIT3: "[TLS] tls_split3 - тройное",
            BypassMethod.QUIC_SPLIT: "[QUIC] quic_split - quic разделение",
            BypassMethod.QUIC_SPLIT2: "[QUIC] quic_split2 - двойное",
            BypassMethod.QUIC_SPLIT3: "[QUIC] quic_split3 - тройное",
            BypassMethod.RANDOM: "[СЛУЧАЙНЫЙ] random - случайный",
            BypassMethod.RANDOM2: "[СЛУЧАЙНЫЙ] random2 - двойной случайный",
            BypassMethod.RANDOM3: "[СЛУЧАЙНЫЙ] random3 - тройной",
            BypassMethod.RANDOM_SPLIT: "[СЛУЧАЙНЫЙ] random_split - случайное разделение",
            BypassMethod.RANDOM_SPLIT2: "[СЛУЧАЙНЫЙ] random_split2 - усиленное",
            BypassMethod.RANDOM_SPLIT3: "[СЛУЧАЙНЫЙ] random_split3 - максимальное",
            BypassMethod.RANDOM_HOLE: "[СЛУЧАЙНЫЙ] random_hole - случайные дыры",
            BypassMethod.RANDOM_FRAG: "[СЛУЧАЙНЫЙ] random_frag - случайная фрагментация",
            BypassMethod.MULTI_FAKE: "[МНОЖЕСТВЕННЫЙ] multi_fake - множ. подмена",
            BypassMethod.MULTI_FAKE2: "[МНОЖЕСТВЕННЫЙ] multi_fake2 - усиленная",
            BypassMethod.MULTI_FAKE3: "[МНОЖЕСТВЕННЫЙ] multi_fake3 - максимальная",
            BypassMethod.MULTI_SPLIT: "[МНОЖЕСТВЕННЫЙ] multi_split - множ. разделение",
            BypassMethod.MULTI_HOLE: "[МНОЖЕСТВЕННЫЙ] multi_hole - множ. дыры",
            BypassMethod.MULTI_FRAG: "[МНОЖЕСТВЕННЫЙ] multi_frag - множ. фрагментация",
            BypassMethod.MULTI_ALL: "[МНОЖЕСТВЕННЫЙ] multi_all - все множественные",
            BypassMethod.AUTO: "[АВТО] auto - автоматический выбор",
            BypassMethod.AUTO2: "[АВТО] auto2 - усиленный",
            BypassMethod.AUTO3: "[АВТО] auto3 - максимальный",
            BypassMethod.SMART: "[УМНЫЙ] smart - умный выбор",
            BypassMethod.SMART2: "[УМНЫЙ] smart2 - усиленный",
            BypassMethod.SMART3: "[УМНЫЙ] smart3 - максимальный",
            BypassMethod.TLS12: "[ПРОТОКОЛ] tls12 - принудительный tls 1.2",
            BypassMethod.TLS13: "[ПРОТОКОЛ] tls13 - принудительный tls 1.3",
            BypassMethod.TLS_OLD: "[ПРОТОКОЛ] tls_old - старые tls",
            BypassMethod.TLS_NEW: "[ПРОТОКОЛ] tls_new - новые tls",
            BypassMethod.QUIC: "[ПРОТОКОЛ] quic - quic протокол",
            BypassMethod.QUIC_OLD: "[ПРОТОКОЛ] quic_old - старые quic",
            BypassMethod.QUIC_NEW: "[ПРОТОКОЛ] quic_new - новые quic",
            BypassMethod.HTTP: "[ПРОТОКОЛ] http - http",
            BypassMethod.HTTP2: "[ПРОТОКОЛ] http2 - http/2",
            BypassMethod.HTTP3: "[ПРОТОКОЛ] http3 - http/3",
            BypassMethod.HTTPS: "[ПРОТОКОЛ] https - https",
            BypassMethod.WEBSOCKET: "[ПРОТОКОЛ] websocket - websocket",
            BypassMethod.WEBSOCKET2: "[ПРОТОКОЛ] websocket2 - усиленный",
            BypassMethod.WEBSOCKET3: "[ПРОТОКОЛ] websocket3 - максимальный",
            BypassMethod.DNS: "[ПРОТОКОЛ] dns - dns туннелирование",
            BypassMethod.DNS2: "[ПРОТОКОЛ] dns2 - усиленное",
            BypassMethod.DNS3: "[ПРОТОКОЛ] dns3 - максимальное",
            BypassMethod.FAKE_MULTISPLIT: "[КОМБО] fake+multisplit",
            BypassMethod.FAKE_MULTISPLIT_DISORDER: "[КОМБО] fake+multisplit+disorder",
            BypassMethod.FAKE_MULTISPLIT_DISORDER2: "[КОМБО] fake+multisplit+disorder2",
            BypassMethod.FAKE_MULTISPLIT_DISORDER3: "[КОМБО] fake+multisplit+disorder3",
            BypassMethod.FAKE_MULTISPLIT_HOLE: "[КОМБО] fake+multisplit+hole",
            BypassMethod.FAKE_MULTISPLIT_HOLE2: "[КОМБО] fake+multisplit+hole2",
            BypassMethod.FAKE_MULTISPLIT_FRAG: "[КОМБО] fake+multisplit+fragment",
            BypassMethod.FAKE_MULTISPLIT_FRAG2: "[КОМБО] fake+multisplit+fragment2",
            BypassMethod.FAKE_MULTISPLIT_BADSUM: "[КОМБО] fake+multisplit+badsum",
            BypassMethod.FAKE_MULTISPLIT_MD5: "[КОМБО] fake+multisplit+md5sig",
            BypassMethod.FAKE_HOLE: "[КОМБО] fake+hole",
            BypassMethod.FAKE_HOLE2: "[КОМБО] fake+hole2",
            BypassMethod.FAKE_FRAG: "[КОМБО] fake+fragment",
            BypassMethod.FAKE_FRAG2: "[КОМБО] fake+fragment2",
            BypassMethod.FAKE_BADSUM: "[КОМБО] fake+badsum",
            BypassMethod.FAKE_MD5: "[КОМБО] fake+md5sig",
            BypassMethod.MULTISPLIT_HOLE: "[КОМБО] multisplit+hole",
            BypassMethod.MULTISPLIT_HOLE2: "[КОМБО] multisplit+hole2",
            BypassMethod.MULTISPLIT_FRAG: "[КОМБО] multisplit+fragment",
            BypassMethod.MULTISPLIT_FRAG2: "[КОМБО] multisplit+fragment2",
            BypassMethod.MULTISPLIT_BADSUM: "[КОМБО] multisplit+badsum",
            BypassMethod.DISORDER_HOLE: "[КОМБО] disorder+hole",
            BypassMethod.DISORDER2_HOLE: "[КОМБО] disorder2+hole",
            BypassMethod.DISORDER3_HOLE: "[КОМБО] disorder3+hole",
            BypassMethod.FRAG_HOLE: "[КОМБО] fragment+hole",
            BypassMethod.FRAG2_HOLE: "[КОМБО] fragment2+hole",
            BypassMethod.FRAG3_HOLE: "[КОМБО] fragment3+hole",
            BypassMethod.ALL_BASIC: "[МЕГА] all_basic - все базовые",
            BypassMethod.ALL_ADVANCED: "[МЕГА] all_advanced - все продвинутые",
            BypassMethod.ALL_EXTREME: "[МЕГА] all_extreme - все экстремальные",
            BypassMethod.ALL_ULTIMATE: "[МЕГА] all_ultimate - все ультимативные",
            BypassMethod.ALL_MAX: "[МЕГА] all_max - все максимальные",
            BypassMethod.ALL_INSANE: "[МЕГА] all_insane - все безумные",
            BypassMethod.ALL_GOD: "[МЕГА] all_god - все божественные",
            BypassMethod.ADVANCED1: "[ПРОДВИНУТЫЙ] advanced1",
            BypassMethod.ADVANCED2: "[ПРОДВИНУТЫЙ] advanced2",
            BypassMethod.ADVANCED3: "[ПРОДВИНУТЫЙ] advanced3",
            BypassMethod.ADVANCED4: "[ПРОДВИНУТЫЙ] advanced4",
            BypassMethod.ADVANCED5: "[ПРОДВИНУТЫЙ] advanced5",
            BypassMethod.ADVANCED6: "[ПРОДВИНУТЫЙ] advanced6",
            BypassMethod.ADVANCED7: "[ПРОДВИНУТЫЙ] advanced7",
            BypassMethod.ADVANCED8: "[ПРОДВИНУТЫЙ] advanced8",
            BypassMethod.ADVANCED9: "[ПРОДВИНУТЫЙ] advanced9",
            BypassMethod.ADVANCED10: "[ПРОДВИНУТЫЙ] advanced10",
            BypassMethod.STEALTH1: "[СТЕЛС] stealth1",
            BypassMethod.STEALTH2: "[СТЕЛС] stealth2",
            BypassMethod.STEALTH3: "[СТЕЛС] stealth3",
            BypassMethod.STEALTH4: "[СТЕЛС] stealth4",
            BypassMethod.STEALTH5: "[СТЕЛС] stealth5",
            BypassMethod.STEALTH6: "[СТЕЛС] stealth6",
            BypassMethod.STEALTH7: "[СТЕЛС] stealth7",
            BypassMethod.STEALTH8: "[СТЕЛС] stealth8",
            BypassMethod.STEALTH9: "[СТЕЛС] stealth9",
            BypassMethod.STEALTH10: "[СТЕЛС] stealth10",
            BypassMethod.GAMING1: "[ИГРОВОЙ] gaming1",
            BypassMethod.GAMING2: "[ИГРОВОЙ] gaming2",
            BypassMethod.GAMING3: "[ИГРОВОЙ] gaming3",
            BypassMethod.GAMING4: "[ИГРОВОЙ] gaming4",
            BypassMethod.GAMING5: "[ИГРОВОЙ] gaming5",
            BypassMethod.GAMING6: "[ИГРОВОЙ] gaming6",
            BypassMethod.GAMING7: "[ИГРОВОЙ] gaming7",
            BypassMethod.GAMING8: "[ИГРОВОЙ] gaming8",
            BypassMethod.GAMING9: "[ИГРОВОЙ] gaming9",
            BypassMethod.GAMING10: "[ИГРОВОЙ] gaming10",
            BypassMethod.YOUTUBE: "[САЙТ] youtube - оптимизация youtube",
            BypassMethod.YOUTUBE2: "[САЙТ] youtube2 - усиленная",
            BypassMethod.YOUTUBE3: "[САЙТ] youtube3 - максимальная",
            BypassMethod.NETFLIX: "[САЙТ] netflix - оптимизация netflix",
            BypassMethod.NETFLIX2: "[САЙТ] netflix2 - усиленная",
            BypassMethod.NETFLIX3: "[САЙТ] netflix3 - максимальная",
            BypassMethod.TWITCH: "[САЙТ] twitch - оптимизация twitch",
            BypassMethod.TWITCH2: "[САЙТ] twitch2 - усиленная",
            BypassMethod.TWITCH3: "[САЙТ] twitch3 - максимальная",
            BypassMethod.DISCORD: "[САЙТ] discord - оптимизация discord",
            BypassMethod.DISCORD2: "[САЙТ] discord2 - усиленная",
            BypassMethod.DISCORD3: "[САЙТ] discord3 - максимальная",
            BypassMethod.TELEGRAM: "[САЙТ] telegram - оптимизация telegram",
            BypassMethod.TELEGRAM2: "[САЙТ] telegram2 - усиленная",
            BypassMethod.TELEGRAM3: "[САЙТ] telegram3 - максимальная",
            BypassMethod.EXPERIMENTAL1: "[ЭКСП] experimental1",
            BypassMethod.EXPERIMENTAL2: "[ЭКСП] experimental2",
            BypassMethod.EXPERIMENTAL3: "[ЭКСП] experimental3",
            BypassMethod.EXPERIMENTAL4: "[ЭКСП] experimental4",
            BypassMethod.EXPERIMENTAL5: "[ЭКСП] experimental5",
            BypassMethod.BETA1: "[БЕТА] beta1",
            BypassMethod.BETA2: "[БЕТА] beta2",
            BypassMethod.BETA3: "[БЕТА] beta3",
            BypassMethod.ALPHA1: "[АЛЬФА] alpha1",
            BypassMethod.ALPHA2: "[АЛЬФА] alpha2",
            BypassMethod.ALPHA3: "[АЛЬФА] alpha3",
            BypassMethod.TEST1: "[ТЕСТ] test1",
            BypassMethod.TEST2: "[ТЕСТ] test2",
            BypassMethod.TEST3: "[ТЕСТ] test3",
            BypassMethod.TEST4: "[ТЕСТ] test4",
            BypassMethod.TEST5: "[ТЕСТ] test5",
            BypassMethod.DEBUG1: "[ОТЛАДКА] debug1",
            BypassMethod.DEBUG2: "[ОТЛАДКА] debug2",
            BypassMethod.DEBUG3: "[ОТЛАДКА] debug3",
        }
        self.method_descriptions = desc
    
    def get_description(self, method: BypassMethod) -> str:
        return self.method_descriptions.get(method, "[НЕИЗВЕСТНО] неизвестный метод")
    
    def get_method_display_name(self, method: BypassMethod) -> str:
        return self.method_descriptions.get(method, f"{method.value} - неизвестный")
    
    def get_all_method_values(self) -> List[str]:
        return [self.get_method_display_name(m) for m in BypassMethod]
    
    def get_method_by_display(self, display_name: str) -> Optional[str]:
        for method in BypassMethod:
            if self.get_method_display_name(method) == display_name:
                return method.value
        return "fake,multisplit,disorder2,hole,fragment,badsum"
    
    def get_methods_count(self) -> int:
        return len(BypassMethod)


class ServiceManager:
    GITHUB_API = "https://api.github.com/repos/bol-van/zapret/releases/latest"
    CURRENT_VERSION = "5.2.0"
    GAME_FILTER_FILES = ["game_filter.txt", "GameFilter.txt", "list-games-ports.txt"]
    
    def __init__(self, base_path: str, log_callback=None):
        self.base_path = base_path
        self._log = log_callback or print
    
    def status_zapret(self) -> Tuple[bool, str]:
        try:
            result = subprocess.run(
                'tasklist /FI "IMAGENAME eq winws_zapret.exe" /NH /FO CSV',
                shell=True,
                capture_output=True,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=5
            )
            lines = [l for l in result.stdout.splitlines() if "winws_zapret.exe" in l]
            if lines:
                parts = lines[0].replace('"', '').split(',')
                pid = parts[1].strip() if len(parts) > 1 else "?"
                mem = parts[4].strip() if len(parts) > 4 else "?"
                return True, f"PID: {pid} | ПАМЯТЬ: {mem}"
            return False, "ПРОЦЕСС НЕ НАЙДЕН"
        except Exception as e:
            return False, f"ОШИБКА: {e}"
    
    def check_updates(self) -> Tuple[bool, str]:
        try:
            headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "Global-Zapret-Pro"}
            resp = requests.get(self.GITHUB_API, headers=headers, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                tag = data.get("tag_name", "").lstrip("v")
                pub = data.get("published_at", "")[:10]
                name = data.get("name", tag)
                return True, f"ПОСЛЕДНИЙ РЕЛИЗ: {name} ({pub})"
            elif resp.status_code == 403:
                return False, "ЛИМИТ GITHUB ПРЕВЫШЕН"
            else:
                return False, f"HTTP {resp.status_code}"
        except requests.exceptions.Timeout:
            return False, "ТАЙМАУТ СОЕДИНЕНИЯ"
        except requests.exceptions.ConnectionError:
            return False, "НЕТ ИНТЕРНЕТА"
        except Exception as e:
            return False, f"ОШИБКА: {e}"
    
    def load_game_filter(self) -> str:
        for filename in self.GAME_FILTER_FILES:
            path = os.path.join(self.base_path, filename)
            if not os.path.exists(path):
                path = os.path.join(self.base_path, "lists", filename)
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    ports = re.findall(r'\d{2,5}(?:-\d{2,5})?', content)
                    if ports:
                        result = ','.join(ports)
                        return result
                except Exception as e:
                    self._log(f"[!] ОШИБКА ЗАГРУЗКИ: {e}")
        return ""
    
    def save_game_filter(self, ports: str):
        path = os.path.join(self.base_path, "game_filter.txt")
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("# НЕОНОВЫЙ ИГРОВОЙ ФИЛЬТР\n")
                f.write(ports + "\n")
        except Exception as e:
            self._log(f"[!] ОШИБКА СОХРАНЕНИЯ: {e}")


class NetworkDiagnostics:
    def __init__(self, log_callback=None):
        self.results = {}
        self.start_time = time.time()
        self.log = log_callback or print
        # Проверяем доступность библиотек
        self.dns_available = False
        self.ping_available = False
        try:
            import dns.resolver
            self.dns_available = True
        except ImportError:
            pass
        try:
            from ping3 import ping
            self.ping_available = True
        except ImportError:
            pass
    
    def check_multiple_dns(self, host: str) -> Dict[str, Tuple[bool, str]]:
        """Проверка DNS через разные серверы"""
        dns_servers = {
            "GOOGLE": "8.8.8.8",
            "CLOUDFLARE": "1.1.1.1",
            "QUAD9": "9.9.9.9",
            "OPENDNS": "208.67.222.222",
            "ADGUARD": "94.140.14.14"
        }
        
        results = {}
        
        if not self.dns_available:
            # Fallback на системный DNS
            try:
                ip = socket.gethostbyname(host)
                results["СИСТЕМНЫЙ"] = (True, f"OK: {ip}")
            except:
                results["СИСТЕМНЫЙ"] = (False, "ОШИБКА")
            return results
        
        import dns.resolver
        import dns.exception
        
        for name, dns_server in dns_servers.items():
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [dns_server]
                resolver.timeout = 3
                resolver.lifetime = 3
                
                answers = resolver.resolve(host, 'A')
                results[name] = (True, f"OK: {answers[0]}")
            except Exception as e:
                results[name] = (False, f"ОШИБКА: {str(e)[:30]}")
            
            time.sleep(0.2)
        
        return results
    
    def check_port_range(self, host: str, ports: List[int], timeout: int = 3) -> Dict[int, Tuple[bool, str]]:
        """Проверка диапазона портов"""
        results = {}
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    results[port] = (True, "ОТКРЫТ")
                else:
                    results[port] = (False, "ЗАКРЫТ/ФИЛЬТР")
            except Exception as e:
                results[port] = (False, f"ОШИБКА: {str(e)[:20]}")
        
        return results
    
    def check_ping(self, host: str, count: int = 4) -> Dict[str, Any]:
        """Проверка ping до хоста"""
        results = {
            "packet_loss": 100,
            "avg_rtt": None,
            "min_rtt": None,
            "max_rtt": None,
            "success": False
        }
        
        if self.ping_available:
            from ping3 import ping
            rtts = []
            for i in range(count):
                try:
                    rtt = ping(host, timeout=2)
                    if rtt is not None:
                        rtts.append(rtt * 1000)  # конвертируем в ms
                except:
                    pass
                time.sleep(0.2)
            
            if rtts:
                results["packet_loss"] = ((count - len(rtts)) / count) * 100
                results["avg_rtt"] = sum(rtts) / len(rtts)
                results["min_rtt"] = min(rtts)
                results["max_rtt"] = max(rtts)
                results["success"] = True
        else:
            # Fallback на системный ping
            try:
                result = subprocess.run(
                    ["ping", "-n", str(count), "-w", "2000", host],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                if "TTL" in result.stdout.upper():
                    results["success"] = True
                    # Парсим потери пакетов
                    loss_match = re.search(r'(\d+)%', result.stdout)
                    if loss_match:
                        results["packet_loss"] = float(loss_match.group(1))
                    # Парсим среднее время
                    avg_match = re.search(r'Среднее = (\d+)', result.stdout)
                    if avg_match:
                        avg = float(avg_match.group(1))
                        results["avg_rtt"] = avg
                        results["min_rtt"] = avg
                        results["max_rtt"] = avg
            except:
                pass
        
        return results
    
    def check_http_advanced(self, url: str, timeout: int = 5) -> Tuple[bool, str, int]:
        """Расширенная проверка HTTP с разными User-Agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'curl/7.68.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        last_status = 0
        last_error = ""
        
        for ua in user_agents:
            try:
                headers = {
                    'User-Agent': ua,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                response = requests.get(
                    url, 
                    headers=headers, 
                    timeout=timeout, 
                    allow_redirects=True,
                    verify=True
                )
                
                if response.status_code == 200:
                    return True, f"HTTP 200 OK", response.status_code
                elif response.status_code in [403, 451, 502, 503, 504]:
                    last_status = response.status_code
                    continue
                else:
                    last_status = response.status_code
                    return False, f"HTTP {response.status_code}", response.status_code
                    
            except requests.exceptions.SSLError as e:
                last_error = f"SSL ОШИБКА: {str(e)[:30]}"
                continue
            except requests.exceptions.Timeout:
                last_error = "ТАЙМАУТ"
                continue
            except requests.exceptions.ConnectionError as e:
                last_error = f"ОШИБКА СОЕДИНЕНИЯ: {str(e)[:30]}"
                continue
            except Exception as e:
                last_error = f"ОШИБКА: {str(e)[:30]}"
                continue
        
        if last_status:
            return False, f"HTTP {last_status}", last_status
        if last_error:
            return False, last_error, 0
        return False, "ВСЕ ПОПЫТКИ НЕУДАЧНЫ", 0
    
    def detect_block_type(self, dns_results: Dict, tcp_results: Dict, http_result: Tuple) -> BlockType:
        """Определение типа блокировки"""
        
        dns_success = any(ok for ok, _ in dns_results.values())
        if not dns_success:
            return BlockType.DNS
        
        tcp_success = any(ok for ok, _ in tcp_results.values() if ok)
        if not tcp_success:
            # Проверяем, открыт ли хоть какой-то порт
            return BlockType.TCP
        
        http_ok, http_msg, http_code = http_result
        if not http_ok:
            if "SSL" in http_msg.upper() or "CERT" in http_msg.upper():
                return BlockType.TLS
            elif http_code in [403, 451]:
                return BlockType.HTTP
            elif http_code in [502, 503, 504]:
                return BlockType.TIMEOUT
            elif http_code in [301, 302, 307, 308]:
                # Редирект может быть нормальным
                return BlockType.UNKNOWN
            else:
                return BlockType.HTTPS
        
        return BlockType.UNKNOWN


class ProcessManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.process: Optional[subprocess.Popen] = None
        self.is_running = False
        self.current_mode = Mode.UNIVERSAL
        
        self.config = ConfigManager()
        self.lists_manager = ListsManager(self.config.base_path)
        self.bypass_manager = BypassMethodManager()
        
        self.packet_config = PacketConfig(
            tcp_ports=self.config.get("packets.tcp_ports", TCP_PORTS),
            udp_ports=self.config.get("packets.udp_ports", UDP_PORTS),
            split_pos=self.config.get("packets.split_pos", 1),
            fooling=self.config.get("packets.fooling", "ts"),
            auto_restart=self.config.get("packets.auto_restart", True),
            fragment_size=self.config.get("packets.fragment_size", 128),
            ttl_min=self.config.get("packets.ttl_min", 32),
            ttl_max=self.config.get("packets.ttl_max", 128),
            window_size=self.config.get("packets.window_size", 65535),
            randomize=self.config.get("packets.randomize", False),
            use_proxy=self.config.get("packets.use_proxy", False),
            proxy_address=self.config.get("packets.proxy_address", "socks5://127.0.0.1:1080"),
            custom_methods=self.config.get("packets.custom_methods", "fake,multisplit,disorder2,hole,fragment,badsum")
        )
        
        self.service_configs = {}
        for service in SERVICES_LIST:
            self.service_configs[service] = ServiceConfig(
                enabled=self.config.get(f"services.{service}.enabled", True)
            )
        
        self.service_configs["discord"].is_discord = True
        self.service_configs["discord"].udp_ports = "19294-19344,50000-50100"
        self.service_configs["general"].is_general = True
        
        self.monitor_thread = None
        self.stop_monitor = threading.Event()
        self.process_lock = threading.Lock()
        self.restart_lock = threading.Lock()
        
        self._load_config()
        self._check_single_instance()
        self._check_drivers()
    
    def _load_config(self):
        mode_map = {
            "ЛАЙТ": Mode.LITE,
            "СТАНДАРТ": Mode.STANDARD,
            "АГРЕССИВ": Mode.AGGRESSIVE,
            "УЛЬТРА": Mode.ULTRA,
            "ПРОИЗВ.": Mode.PERFORMANCE,
            "УНИВЕРС.": Mode.UNIVERSAL,
            "ИГРОВОЙ": Mode.GAMING,
            "СТЕЛС": Mode.STEALTH,
            "ЭКСТРИМ": Mode.EXTREME,
            "РАНДОМ": Mode.RANDOM,
            "МУЛЬТИ": Mode.MULTI
        }
        
        self.current_mode = mode_map.get(self.config.get("mode"), Mode.UNIVERSAL)
        
        services_config = self.config.get("services", {})
        for service in SERVICES_LIST:
            self.service_configs[service].enabled = services_config.get(service, {}).get("enabled", True)
    
    def _check_drivers(self):
        bin_path = os.path.join(self.config.base_path, "bin")
        required_files = [
            "winws_zapret.exe",
            "WinDivert64.sys",
            "WinDivert.dll"
        ]
        
        tls_files = list(TLS_PATTERNS.values()) + ["quic_initial_www_google_com.bin"]
        
        missing_files = []
        for file in required_files + tls_files:
            file_path = os.path.join(bin_path, file)
            if not os.path.exists(file_path):
                missing_files.append(file)
        
        if missing_files:
            error_msg = f"[!] ОТСУТСТВУЮТ ДРАЙВЕРЫ:\n{', '.join(missing_files[:5])}"
            if len(missing_files) > 5:
                error_msg += f"\nИ ЕЩЁ {len(missing_files) - 5} ФАЙЛОВ"
            error_msg += "\n\nПРОГРАММА НЕ МОЖЕТ РАБОТАТЬ!"
            ctypes.windll.user32.MessageBoxW(0, error_msg, "GLOBAL-ZAPRET-PRO ОШИБКА", 0x10 | 0x0)
            sys.exit(1)
    
    def _check_single_instance(self):
        try:
            import win32event
            import win32api
            import winerror
            
            self.mutex = win32event.CreateMutex(None, False, "Global-Zapret-Pro-Instance")
            if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
                ctypes.windll.user32.MessageBoxW(0, 
                    "[!] ПРОГРАММА УЖЕ ЗАПУЩЕНА", 
                    "GLOBAL-ZAPRET-PRO", 
                    0x40 | 0x0)
                sys.exit(0)
        except ImportError:
            self.lock_file = Path(self.config.base_path) / ".instance.lock"
            try:
                if self.lock_file.exists():
                    with open(self.lock_file, 'r') as f:
                        pid = int(f.read().strip())
                    try:
                        os.kill(pid, 0)
                        sys.exit(0)
                    except:
                        pass
                
                with open(self.lock_file, 'w') as f:
                    f.write(str(os.getpid()))
                atexit.register(self._cleanup_lock_file)
            except:
                pass
    
    def _cleanup_lock_file(self):
        try:
            if hasattr(self, 'lock_file') and self.lock_file.exists():
                self.lock_file.unlink()
        except:
            pass
    
    @staticmethod
    def _kill_old_instances():
        try:
            subprocess.run(
                "taskkill /F /IM winws_zapret.exe /T",
                shell=True,
                capture_output=True,
                timeout=3,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            time.sleep(0.5)
        except:
            pass
    
    def _get_ttl_value(self) -> int:
        if self.packet_config.randomize:
            return random.randint(self.packet_config.ttl_min, self.packet_config.ttl_max)
        return self.packet_config.ttl_max
    
    def _get_window_size(self) -> int:
        if self.packet_config.randomize:
            return random.randint(4096, self.packet_config.window_size)
        return self.packet_config.window_size
    
    def _build_command(self) -> List[str]:
        bin_path = os.path.join(self.config.base_path, "bin")
        lists_path = os.path.join(self.config.base_path, "lists")
        exe_path = os.path.join(bin_path, "winws_zapret.exe")
        
        if not os.path.exists(exe_path):
            raise FileNotFoundError("winws_zapret.exe НЕ НАЙДЕН")
        
        profile = DPIProfile.get_default_profiles()[self.current_mode]
        
        desync_method = self.packet_config.custom_methods or \
                        profile.desync.replace("--dpi-desync=", "") or \
                        "fake,multisplit"
        desync_param = f"--dpi-desync={desync_method}"
        
        BAT_FOOLING = "ts"
        BAT_SPLIT_POS = "1"
        BAT_SEQOVL_SVC = "681"
        BAT_SEQOVL_GEN = "664"
        
        game_filter = getattr(self.packet_config, 'game_filter', "")
        
        wf_tcp = f"--wf-tcp={TCP_PORTS}" + (f",{game_filter}" if game_filter else "")
        wf_udp = f"--wf-udp={UDP_PORTS}" + (f",{game_filter}" if game_filter else "")
        cmd = [exe_path, wf_tcp, wf_udp]
        
        if self.packet_config.use_proxy:
            cmd.append(f"--proxy={self.packet_config.proxy_address}")
        
        if self.packet_config.randomize:
            cmd.extend([
                f"--dpi-desync-ttl={self._get_ttl_value()}",
                f"--dpi-desync-window={self._get_window_size()}"
            ])
        
        if "fragment" in desync_method or "fragment" in profile.methods:
            cmd.append(f"--dpi-desync-fragment={self.packet_config.fragment_size}")
        
        if self.service_configs["general"].enabled and \
                self.lists_manager.check_list_exists('list-general.txt'):
            cmd.extend([
                "--filter-udp=443",
                f"--hostlist={os.path.join(lists_path, 'list-general.txt')}",
                f"--hostlist-exclude={os.path.join(lists_path, 'list-exclude.txt')}",
                f"--ipset-exclude={os.path.join(lists_path, 'ipset-exclude.txt')}",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=11",
                f"--dpi-desync-fake-quic={os.path.join(bin_path, 'quic_initial_www_google_com.bin')}",
                "--new"
            ])
        
        if self.service_configs["discord"].enabled:
            cmd.extend([
                "--filter-udp=19294-19344,50000-50100",
                "--filter-l7=discord,stun",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=6",
                "--new"
            ])
        
        if self.service_configs["discord"].enabled:
            cmd.extend([
                "--filter-tcp=2053,2083,2087,2096,8443",
                "--hostlist-domains=discord.media",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_SVC}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=8",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, 'tls_clienthello_www_google_com.bin')}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, 'tls_clienthello_www_google_com.bin')}",
                "--new"
            ])
        
        if self.service_configs["google"].enabled and \
                self.lists_manager.check_list_exists('list-google.txt'):
            cmd.extend([
                f"--filter-tcp={TCP_PORTS}",
                f"--hostlist={os.path.join(lists_path, 'list-google.txt')}",
                "--ip-id=zero",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_SVC}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=8",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, TLS_PATTERNS['google'])}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, TLS_PATTERNS['google'])}",
                "--new"
            ])
        
        if self.service_configs["meta"].enabled and \
                self.lists_manager.check_list_exists('list-meta.txt'):
            cmd.extend([
                f"--filter-tcp={TCP_PORTS}",
                f"--hostlist={os.path.join(lists_path, 'list-meta.txt')}",
                "--ip-id=zero",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_SVC}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=10",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, TLS_PATTERNS['meta'])}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, TLS_PATTERNS['meta'])}",
                "--new"
            ])
        
        if self.service_configs["x"].enabled and \
                self.lists_manager.check_list_exists('list-x.txt'):
            cmd.extend([
                f"--filter-tcp={TCP_PORTS}",
                f"--hostlist={os.path.join(lists_path, 'list-x.txt')}",
                "--ip-id=zero",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_SVC}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=8",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, TLS_PATTERNS['x'])}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, TLS_PATTERNS['x'])}",
                "--new"
            ])
        
        if self.service_configs["tiktok"].enabled and \
                self.lists_manager.check_list_exists('list-tiktok.txt'):
            cmd.extend([
                f"--filter-tcp={TCP_PORTS}",
                f"--hostlist={os.path.join(lists_path, 'list-tiktok.txt')}",
                "--ip-id=zero",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_SVC}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=8",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, TLS_PATTERNS['tiktok'])}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, TLS_PATTERNS['tiktok'])}",
                "--new"
            ])
        
        if self.service_configs["telegram"].enabled and \
                self.lists_manager.check_list_exists('list-telegram.txt'):
            cmd.extend([
                f"--filter-tcp={TCP_PORTS}",
                f"--hostlist={os.path.join(lists_path, 'list-telegram.txt')}",
                "--ip-id=zero",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_SVC}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=8",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, TLS_PATTERNS['telegram'])}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, TLS_PATTERNS['telegram'])}",
                "--new"
            ])
        
        if self.service_configs["mylist"].enabled and \
                self.lists_manager.check_list_exists('list-mylist.txt'):
            cmd.extend([
                f"--filter-tcp={TCP_PORTS}",
                f"--hostlist={os.path.join(lists_path, 'list-mylist.txt')}",
                "--ip-id=zero",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_SVC}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=8",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, TLS_PATTERNS['mylist'])}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, TLS_PATTERNS['mylist'])}",
                "--new"
            ])
        
        if self.service_configs["games"].enabled and \
                self.lists_manager.check_list_exists('list-games.txt'):
            cmd.extend([
                f"--filter-tcp={TCP_PORTS}",
                f"--hostlist={os.path.join(lists_path, 'list-games.txt')}",
                "--ip-id=zero",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_SVC}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=4",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, TLS_PATTERNS['games'])}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, TLS_PATTERNS['games'])}",
                "--new"
            ])
        
        if self.service_configs["general"].enabled and \
                self.lists_manager.check_list_exists('list-general.txt'):
            cmd.extend([
                "--filter-tcp=80,443",
                f"--hostlist={os.path.join(lists_path, 'list-general.txt')}",
                f"--hostlist-exclude={os.path.join(lists_path, 'list-exclude.txt')}",
                f"--ipset-exclude={os.path.join(lists_path, 'ipset-exclude.txt')}",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_GEN}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=8",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, TLS_PATTERNS['general'])}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, TLS_PATTERNS['general'])}",
                f"--dpi-desync-fake-http={os.path.join(bin_path, TLS_PATTERNS['general'])}",
                "--new"
            ])
        
        if self.lists_manager.check_list_exists('ipset-all.txt'):
            cmd.extend([
                "--filter-udp=443",
                f"--ipset={os.path.join(lists_path, 'ipset-all.txt')}",
                f"--hostlist-exclude={os.path.join(lists_path, 'list-exclude.txt')}",
                f"--ipset-exclude={os.path.join(lists_path, 'ipset-exclude.txt')}",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=11",
                f"--dpi-desync-fake-quic={os.path.join(bin_path, 'quic_initial_www_google_com.bin')}",
                "--new"
            ])
        
        if self.lists_manager.check_list_exists('ipset-all.txt'):
            ipset_tcp = f"80,443,{game_filter}" if game_filter else "80,443"
            cmd.extend([
                f"--filter-tcp={ipset_tcp}",
                f"--ipset={os.path.join(lists_path, 'ipset-all.txt')}",
                f"--hostlist-exclude={os.path.join(lists_path, 'list-exclude.txt')}",
                f"--ipset-exclude={os.path.join(lists_path, 'ipset-exclude.txt')}",
                desync_param,
                f"--dpi-desync-split-seqovl={BAT_SEQOVL_GEN}",
                f"--dpi-desync-split-pos={BAT_SPLIT_POS}",
                f"--dpi-desync-fooling={BAT_FOOLING}",
                "--dpi-desync-repeats=8",
                f"--dpi-desync-split-seqovl-pattern={os.path.join(bin_path, TLS_PATTERNS['general'])}",
                f"--dpi-desync-fake-tls={os.path.join(bin_path, TLS_PATTERNS['general'])}",
                f"--dpi-desync-fake-http={os.path.join(bin_path, TLS_PATTERNS['general'])}",
                "--new"
            ])
        
        if game_filter and self.lists_manager.check_list_exists('ipset-all.txt'):
            cmd.extend([
                f"--filter-udp={game_filter}",
                f"--ipset={os.path.join(lists_path, 'ipset-all.txt')}",
                f"--ipset-exclude={os.path.join(lists_path, 'ipset-exclude.txt')}",
                "--dpi-desync=fake",
                "--dpi-desync-repeats=10",
                "--dpi-desync-any-protocol=1",
                f"--dpi-desync-fake-unknown-udp={os.path.join(bin_path, 'quic_initial_www_google_com.bin')}",
                "--dpi-desync-cutoff=n4"
            ])
        
        return cmd
    
    def start(self) -> bool:
        with self.process_lock:
            try:
                self._kill_old_instances()
                cmd = self._build_command()
                
                self.process = subprocess.Popen(
                    cmd,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                self.is_running = True
                self.stop_monitor.clear()
                
                if not self.monitor_thread or not self.monitor_thread.is_alive():
                    self.monitor_thread = threading.Thread(
                        target=self._monitor_process,
                        daemon=True
                    )
                    self.monitor_thread.start()
                
                return True
                
            except Exception as e:
                print(f"[!] ОШИБКА ЗАПУСКА: {e}")
                self.is_running = False
                return False
    
    def _monitor_process(self):
        while not self.stop_monitor.is_set() and self.is_running:
            if self.process:
                retcode = self.process.poll()
                if retcode is not None:
                    if self.is_running:
                        time.sleep(2)
                        if self.packet_config.auto_restart:
                            self.start()
                    break
            time.sleep(1)
    
    def stop(self):
        with self.process_lock:
            self.stop_monitor.set()
            self.is_running = False
            
            if self.process:
                try:
                    self.process.terminate()
                    time.sleep(0.5)
                    self.process.kill()
                except:
                    pass
                self.process = None
            
            self._kill_old_instances()
    
    def restart(self) -> bool:
        with self.restart_lock:
            self.stop()
            time.sleep(1)
            return self.start()
    
    def set_mode(self, mode: Mode):
        with self.process_lock:
            self.current_mode = mode
            if self.is_running:
                threading.Thread(target=self.restart, daemon=True).start()
    
    def set_service_enabled(self, service: str, enabled: bool):
        with self.process_lock:
            if service in self.service_configs:
                self.service_configs[service].enabled = enabled
                if self.is_running:
                    threading.Thread(target=self.restart, daemon=True).start()
    
    def update_packet_config(self, config: PacketConfig):
        with self.process_lock:
            self.packet_config = config
            self.config.set("packets.tcp_ports", config.tcp_ports)
            self.config.set("packets.udp_ports", config.udp_ports)
            self.config.set("packets.split_pos", config.split_pos)
            self.config.set("packets.fooling", config.fooling)
            self.config.set("packets.auto_restart", config.auto_restart)
            self.config.set("packets.fragment_size", config.fragment_size)
            self.config.set("packets.ttl_min", config.ttl_min)
            self.config.set("packets.ttl_max", config.ttl_max)
            self.config.set("packets.window_size", config.window_size)
            self.config.set("packets.randomize", config.randomize)
            self.config.set("packets.use_proxy", config.use_proxy)
            self.config.set("packets.proxy_address", config.proxy_address)
            self.config.set("packets.custom_methods", config.custom_methods)
            
            if self.is_running and config.auto_restart:
                threading.Thread(target=self.restart, daemon=True).start()


# ==============================================================================
# НОВОЕ ОКНО АВТО-ПОДБОРА ОБХОДА
# ==============================================================================

class AutoBypassWindow(ctk.CTkToplevel, NeonBaseWindow):
    """Окно авто-подбора метода обхода на основе диагностики"""
    
    def __init__(self, parent, diagnostics_data: dict, log_callback):
        super().__init__(parent)
        NeonBaseWindow.__init__(self, self)
        
        self.diagnostics_data = diagnostics_data
        self.log = log_callback
        self.parent = parent
        self.bypass_manager = BypassMethodManager()
        
        self.title("⚡ GLOBAL-ZAPRET-PRO :: АВТО-ПОДБОР ОБХОДА ⚡")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        self._create_neon_header(self, "АВТОМАТИЧЕСКИЙ ПОДБОР", "РЕКОМЕНДАЦИИ НА ОСНОВЕ ДИАГНОСТИКИ")
        
        main_frame = ctk.CTkFrame(
            self, 
            fg_color=NEON_THEME['bg_secondary'], 
            corner_radius=8,
            border_width=2,
            border_color=NEON_THEME['primary']
        )
        main_frame.pack(pady=8, padx=12, fill="both", expand=True)
        
        # Данные диагностики
        data_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        data_frame.pack(pady=12, padx=12, fill="x")
        
        target_label = ctk.CTkLabel(
            data_frame,
            text=f"🎯 ЦЕЛЬ: {self.diagnostics_data.get('target', 'НЕИЗВЕСТНО')}",
            font=("Courier New", 13, "bold"),
            text_color=NEON_THEME['primary']
        )
        target_label.pack(anchor="w", pady=(0, 8))
        
        # Тип блокировки
        block_type = self.diagnostics_data.get('block_type', 'UNKNOWN')
        block_color = NEON_THEME['error'] if block_type != 'UNKNOWN' else NEON_THEME['success']
        
        block_frame = ctk.CTkFrame(data_frame, fg_color=NEON_THEME['bg_tertiary'], corner_radius=6)
        block_frame.pack(fill="x", pady=4)
        
        block_label = ctk.CTkLabel(
            block_frame,
            text=f"🚫 ТИП БЛОКИРОВКИ: {block_type}",
            font=("Courier New", 12, "bold"),
            text_color=block_color
        )
        block_label.pack(pady=6, padx=8)
        
        # Рекомендованные режимы
        rec_label = ctk.CTkLabel(
            data_frame,
            text="💡 РЕКОМЕНДОВАННЫЕ РЕЖИМЫ:",
            font=("Courier New", 12, "bold"),
            text_color=NEON_THEME['secondary']
        )
        rec_label.pack(anchor="w", pady=(12, 4))
        
        recommended_modes = self._get_recommended_modes(block_type)
        
        modes_frame = ctk.CTkFrame(data_frame, fg_color=NEON_THEME['bg_tertiary'], corner_radius=6)
        modes_frame.pack(fill="x", pady=4)
        
        for i, mode in enumerate(recommended_modes):
            mode_color = NEON_THEME['primary'] if i == 0 else NEON_THEME['text_secondary']
            mode_label = ctk.CTkLabel(
                modes_frame,
                text=f"{'→' if i == 0 else '•'} {mode}",
                font=("Courier New", 11),
                text_color=mode_color
            )
            mode_label.pack(anchor="w", pady=2, padx=12)
        
        # Рекомендованные методы
        method_label = ctk.CTkLabel(
            data_frame,
            text="🎭 РЕКОМЕНДОВАННЫЕ МЕТОДЫ:",
            font=("Courier New", 12, "bold"),
            text_color=NEON_THEME['secondary']
        )
        method_label.pack(anchor="w", pady=(12, 4))
        
        recommended_methods = self._get_recommended_methods(block_type)
        
        methods_frame = ctk.CTkFrame(data_frame, fg_color=NEON_THEME['bg_tertiary'], corner_radius=6)
        methods_frame.pack(fill="x", pady=4)
        
        for i, method in enumerate(recommended_methods[:5]):  # Показываем топ-5
            method_text = self.bypass_manager.get_method_display_name(method) if hasattr(self, 'bypass_manager') else method.value
            method_label = ctk.CTkLabel(
                methods_frame,
                text=f"• {method_text}",
                font=("Courier New", 10),
                text_color=NEON_THEME['text_secondary']
            )
            method_label.pack(anchor="w", pady=2, padx=12)
        
        # Кнопки действий
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(pady=15, padx=12, fill="x")
        
        row1 = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        row1.pack(fill="x", pady=4)
        
        apply_mode_btn = ctk.CTkButton(
            row1,
            text=f"▶ ПРИМЕНИТЬ {recommended_modes[0]}",
            command=lambda: self._apply_recommended_mode(recommended_modes[0]),
            height=35,
            corner_radius=6,
            fg_color=NEON_THEME['primary'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 12, "bold")
        )
        apply_mode_btn.pack(side="left", padx=(0, 4), expand=True, fill="x")
        
        open_packets_btn = ctk.CTkButton(
            row1,
            text="📦 ОТКРЫТЬ ПАКЕТЫ",
            command=self._open_packets,
            height=35,
            corner_radius=6,
            fg_color=NEON_THEME['warning'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 12, "bold")
        )
        open_packets_btn.pack(side="right", padx=(4, 0), expand=True, fill="x")
        
        row2 = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        row2.pack(fill="x", pady=4)
        
        save_report_btn = ctk.CTkButton(
            row2,
            text="💾 СОХРАНИТЬ ОТЧЕТ",
            command=self._save_report,
            height=35,
            corner_radius=6,
            fg_color=NEON_THEME['success'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 12, "bold")
        )
        save_report_btn.pack(side="left", padx=(0, 4), expand=True, fill="x")
        
        close_btn = ctk.CTkButton(
            row2,
            text="✕ ЗАКРЫТЬ",
            command=self.destroy,
            height=35,
            corner_radius=6,
            fg_color=NEON_THEME['error'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 12, "bold")
        )
        close_btn.pack(side="right", padx=(4, 0), expand=True, fill="x")
    
    def _get_recommended_modes(self, block_type: str) -> List[str]:
        """Получение рекомендованных режимов на основе типа блокировки"""
        recommendations = {
            "DNS": ["СТАНДАРТ", "УНИВЕРС.", "ЛАЙТ"],
            "TCP": ["УНИВЕРС.", "АГРЕССИВ", "МУЛЬТИ"],
            "HTTP": ["СТАНДАРТ", "УНИВЕРС.", "ЛАЙТ"],
            "HTTPS": ["АГРЕССИВ", "УЛЬТРА", "ЭКСТРИМ"],
            "TLS": ["УЛЬТРА", "ЭКСТРИМ", "МУЛЬТИ"],
            "TIMEOUT": ["УНИВЕРС.", "СТАНДАРТ", "ЛАЙТ"],
            "UNKNOWN": ["УНИВЕРС.", "СТАНДАРТ", "АГРЕССИВ"]
        }
        return recommendations.get(block_type, ["УНИВЕРС.", "СТАНДАРТ", "АГРЕССИВ"])
    
    def _get_recommended_methods(self, block_type: str) -> List[BypassMethod]:
        """Получение рекомендованных методов на основе типа блокировки"""
        recommendations = {
            "DNS": [BypassMethod.DNS, BypassMethod.DNS2, BypassMethod.DNS3],
            "TCP": [BypassMethod.MULTISPLIT, BypassMethod.SPLIT2, BypassMethod.DISORDER],
            "HTTP": [BypassMethod.FAKE, BypassMethod.FAKE2, BypassMethod.MIMIC_HTTP],
            "HTTPS": [BypassMethod.FAKE_MULTISPLIT, BypassMethod.TLS_SPLIT, BypassMethod.FRAGMENT],
            "TLS": [BypassMethod.TLS_SPLIT, BypassMethod.TLS_SPLIT2, BypassMethod.FRAGMENT2],
            "TIMEOUT": [BypassMethod.TTL, BypassMethod.TTL_RANDOM, BypassMethod.WSIZE],
            "UNKNOWN": [BypassMethod.FAKE_MULTISPLIT, BypassMethod.ALL_BASIC, BypassMethod.UNIVERSAL]
        }
        return recommendations.get(block_type, [BypassMethod.FAKE_MULTISPLIT, BypassMethod.ALL_BASIC])
    
    def _apply_recommended_mode(self, mode_name: str):
        """Применение рекомендованного режима"""
        if hasattr(self.parent, '_change_mode'):
            self.parent._change_mode(mode_name)
            self.log(f"[АВТО-ПОДБОР] ПРИМЕНЕН РЕЖИМ: {mode_name}")
        self.destroy()
    
    def _open_packets(self):
        """Открытие окна настроек пакетов"""
        if hasattr(self.parent, '_open_packets'):
            self.parent._open_packets()
    
    def _save_report(self):
        """Сохранение отчета диагностики"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"diagnostic_report_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("GLOBAL-ZAPRET-PRO ДИАГНОСТИЧЕСКИЙ ОТЧЕТ\n")
                f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                for key, value in self.diagnostics_data.items():
                    f.write(f"{key}: {value}\n")
            
            self.log(f"[ОТЧЕТ] СОХРАНЕН В {filename}")
        except Exception as e:
            self.log(f"[ОШИБКА] СОХРАНЕНИЕ ОТЧЕТА: {e}")


# ==============================================================================
# ОКНА
# ==============================================================================

class DiagnosticsWindow(ctk.CTkToplevel, NeonBaseWindow):
    """Окно диагностики в неоновом стиле"""
    
    def __init__(self, parent, log_callback):
        super().__init__(parent)
        NeonBaseWindow.__init__(self, self)
        
        self.log = log_callback
        self.diagnostics = NetworkDiagnostics(log_callback)
        self.parent = parent
        
        self.title("⚡ GLOBAL-ZAPRET-PRO :: ДИАГНОСТИКА ⚡")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        self._create_neon_header(self, "ДИАГНОСТИКА СЕТИ", "АНАЛИЗ БЛОКИРОВОК")
        
        main_frame = ctk.CTkFrame(
            self, 
            fg_color=NEON_THEME['bg_secondary'], 
            corner_radius=8,
            border_width=2,
            border_color=NEON_THEME['primary']
        )
        main_frame.pack(pady=8, padx=12, fill="both", expand=True)
        
        select_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        select_frame.pack(pady=8, padx=8, fill="x")
        
        select_label = ctk.CTkLabel(
            select_frame,
            text="🎯 ЦЕЛЕВОЙ СЕРВИС:",
            font=("Courier New", 11, "bold"),
            text_color=NEON_THEME['primary']
        )
        select_label.pack(anchor="w", pady=(0, 4))
        
        self.service_var = ctk.StringVar(value="Google")
        service_menu = ctk.CTkOptionMenu(
            select_frame,
            values=["Google", "Facebook", "Twitter/X", "Telegram", "Instagram", 
                   "YouTube", "Discord", "TikTok", "СВОЙ URL"],
            variable=self.service_var,
            font=("Courier New", 10),
            height=30,
            fg_color=NEON_THEME['bg_tertiary'],
            button_color=NEON_THEME['primary'],
            button_hover_color=NEON_THEME['secondary'],
            dropdown_fg_color=NEON_THEME['bg_secondary'],
            dropdown_hover_color=NEON_THEME['bg_tertiary'],
            text_color=NEON_THEME['text_primary']
        )
        service_menu.pack(fill="x", pady=(0, 4))
        
        self.custom_url_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        self.custom_url_frame.pack(fill="x", pady=(4, 0))
        
        self.custom_url_entry = ctk.CTkEntry(
            self.custom_url_frame,
            placeholder_text="https://example.com",
            font=("Courier New", 10),
            height=30,
            fg_color=NEON_THEME['bg_tertiary'],
            border_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary']
        )
        self.custom_url_entry.pack(fill="x")
        self.custom_url_frame.pack_forget()
        
        service_menu.configure(command=self._on_service_change)
        
        btn_frame = ctk.CTkFrame(select_frame, fg_color="transparent")
        btn_frame.pack(pady=(8, 0), fill="x")
        
        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="🔍 НАЧАТЬ ДИАГНОСТИКУ",
            command=self._start_diagnostics,
            height=35,
            corner_radius=6,
            fg_color=NEON_THEME['primary'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 12, "bold")
        )
        self.start_btn.pack(expand=True, fill="x")
        
        self.progress = ctk.CTkProgressBar(
            main_frame, 
            fg_color=NEON_THEME['bg_tertiary'], 
            progress_color=NEON_THEME['primary'],
            height=8
        )
        self.progress.pack(pady=(8, 0), padx=8, fill="x")
        self.progress.set(0)
        
        # Фрейм с результатами
        result_label = ctk.CTkLabel(
            main_frame,
            text="📊 РЕЗУЛЬТАТЫ АНАЛИЗА",
            font=("Courier New", 12, "bold"),
            text_color=NEON_THEME['secondary']
        )
        result_label.pack(pady=(8, 4))
        
        self.result_text = ctk.CTkTextbox(
            main_frame,
            height=180,
            font=("Courier New", 10),
            fg_color=NEON_THEME['bg_primary'],
            border_color=NEON_THEME['primary'],
            border_width=2,
            text_color=NEON_THEME['text_primary']
        )
        self.result_text.pack(pady=4, padx=8, fill="both", expand=True)
        
        # Кнопка авто-подбора
        auto_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        auto_frame.pack(pady=8, padx=8, fill="x")
        
        self.auto_btn = ctk.CTkButton(
            auto_frame,
            text="🤖 АВТО-ПОДБОР ОБХОДА",
            command=self._open_auto_bypass,
            height=30,
            corner_radius=6,
            fg_color=NEON_THEME['tertiary'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 11, "bold"),
            state="disabled"
        )
        self.auto_btn.pack(expand=True, fill="x")
        
        rec_label = ctk.CTkLabel(
            main_frame,
            text="💡 РЕКОМЕНДАЦИИ",
            font=("Courier New", 12, "bold"),
            text_color=NEON_THEME['secondary']
        )
        rec_label.pack(pady=(4, 4))
        
        self.recommend_text = ctk.CTkTextbox(
            main_frame,
            height=80,
            font=("Courier New", 10),
            fg_color=NEON_THEME['bg_primary'],
            border_color=NEON_THEME['success'],
            border_width=2,
            text_color=NEON_THEME['success']
        )
        self.recommend_text.pack(pady=4, padx=8, fill="x")
        
        self.diagnostic_active = False
        self.last_diagnostics_data = {}
    
    def _on_service_change(self, choice):
        if choice == "СВОЙ URL":
            self.custom_url_frame.pack(fill="x", pady=(4, 0))
        else:
            self.custom_url_frame.pack_forget()
    
    def _start_diagnostics(self):
        if self.diagnostic_active:
            return
        
        self.result_text.delete("1.0", "end")
        self.recommend_text.delete("1.0", "end")
        self.auto_btn.configure(state="disabled")
        
        service = self.service_var.get()
        
        services = {
            "Google": "https://www.google.com",
            "Facebook": "https://www.facebook.com",
            "Twitter/X": "https://twitter.com",
            "Telegram": "https://web.telegram.org",
            "Instagram": "https://www.instagram.com",
            "YouTube": "https://www.youtube.com",
            "Discord": "https://discord.com",
            "TikTok": "https://www.tiktok.com"
        }
        
        if service == "СВОЙ URL":
            url = self.custom_url_entry.get().strip()
            if not url:
                self._add_result("❌ ВВЕДИТЕ URL")
                return
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
        else:
            url = services.get(service, "https://www.google.com")
        
        self.diagnostic_active = True
        self.start_btn.configure(state="disabled", text="⏳ ДИАГНОСТИКА...")
        self.progress.set(0.1)
        
        threading.Thread(target=self._run_diagnostics, args=(url, service), daemon=True).start()
    
    def _run_diagnostics(self, url: str, service_name: str):
        """Запуск диагностики"""
        try:
            parsed = urlparse(url)
            host = parsed.hostname or parsed.path
            
            self._add_result(f"\n{'═'*50}")
            self._add_result(f"🎯 ЦЕЛЬ: {service_name} [{host}]")
            self._add_result(f"{'═'*50}\n")
            
            # DNS проверка
            self._update_progress(0.2, "DNS СКАН...")
            self._add_result("📡 DNS СЕРВЕРЫ:")
            dns_results = self.diagnostics.check_multiple_dns(host)
            dns_success = False
            for server, (ok, msg) in dns_results.items():
                status = "✅" if ok else "❌"
                self._add_result(f"  {status} {server}: {msg}")
                if ok:
                    dns_success = True
            
            # Ping проверка
            self._update_progress(0.4, "PING АНАЛИЗ...")
            self._add_result("\n📊 PING АНАЛИЗ:")
            ping_results = self.diagnostics.check_ping(host)
            if ping_results.get("success", False):
                loss = ping_results.get("packet_loss", 100)
                self._add_result(f"  📦 ПОТЕРИ: {loss:.1f}%")
                if ping_results.get("avg_rtt"):
                    avg = ping_results.get("avg_rtt")
                    self._add_result(f"  ⏱️ СР. ЗАДЕРЖКА: {avg:.1f}ms")
                status = "✅" if loss < 50 else "⚠️"
                self._add_result(f"  {status} PING ДОСТУПЕН")
            else:
                self._add_result("  ❌ PING НЕДОСТУПЕН")
            
            if dns_success:
                # TCP порты
                self._update_progress(0.6, "СКАН ПОРТОВ...")
                self._add_result("\n🔌 TCP ПОРТЫ:")
                all_ports = [80, 443, 8080, 8443, 5222]
                tcp_results = self.diagnostics.check_port_range(host, all_ports)
                tcp_success = False
                for port, (ok, msg) in tcp_results.items():
                    status = "✅" if ok else "❌"
                    self._add_result(f"  {status} ПОРТ {port}: {msg}")
                    if ok:
                        tcp_success = True
                
                # HTTP проверка
                self._update_progress(0.8, "HTTP АНАЛИЗ...")
                self._add_result("\n🌐 HTTP ПРОТОКОЛ:")
                http_ok, http_msg, http_code = self.diagnostics.check_http_advanced(url)
                status = "✅" if http_ok else "❌"
                self._add_result(f"  {status} {http_msg}")
                
                # Определение типа блокировки
                block_type = self.diagnostics.detect_block_type(
                    dns_results, tcp_results, (http_ok, http_msg, http_code)
                )
                
                self._add_result(f"\n{'═'*50}")
                if block_type != BlockType.UNKNOWN:
                    self._add_result(f"🚫 ТИП БЛОКИРОВКИ: {block_type.value}")
                    
                    # Сохраняем данные для авто-подбора
                    self.last_diagnostics_data = {
                        'target': f"{service_name} [{host}]",
                        'block_type': block_type.value,
                        'dns_results': dns_results,
                        'tcp_results': tcp_results,
                        'http_result': (http_ok, http_msg, http_code),
                        'ping_results': ping_results
                    }
                    
                    # Включаем кнопку авто-подбора
                    self.after(0, lambda: self.auto_btn.configure(state="normal"))
                    
                    self._generate_recommendations(block_type, service_name)
                else:
                    self._add_result("✅ СТАТУС: ДОСТУПЕН")
                    self._add_recommendation("ЦЕЛЕВОЙ СЕРВИС ДОСТУПЕН")
            
            elapsed = time.time() - self.diagnostics.start_time
            self._add_result(f"\n⏱️ ВРЕМЯ СКАНА: {elapsed:.1f}с")
            
        except Exception as e:
            self._add_result(f"\n❌ ОШИБКА: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            self.diagnostic_active = False
            self.start_btn.configure(state="normal", text="🔍 НАЧАТЬ ДИАГНОСТИКУ")
            self.progress.set(1)
    
    def _update_progress(self, value: float, status: str):
        self.progress.set(value)
        self.start_btn.configure(text=f"⏳ {status}")
    
    def _add_result(self, text: str):
        def add():
            self.result_text.insert("end", text + "\n")
            self.result_text.see("end")
        self.after(0, add)
    
    def _add_recommendation(self, text: str):
        def add():
            self.recommend_text.insert("end", "• " + text + "\n")
            self.recommend_text.see("end")
        self.after(0, add)
    
    def _generate_recommendations(self, block_type: BlockType, service: str):
        """Генерация рекомендаций на основе типа блокировки"""
        self._add_result("\n💡 РЕКОМЕНДАЦИИ:")
        
        recommendations = {
            BlockType.DNS: [
                "ИСПОЛЬЗУЙТЕ АЛЬТЕРНАТИВНЫЙ DNS (1.1.1.1, 8.8.8.8)",
                "ВКЛЮЧИТЕ DNS-OVER-HTTPS В БРАУЗЕРЕ",
                "АКТИВИРУЙТЕ ВСЕ СЕРВИСЫ В НАСТРОЙКАХ"
            ],
            BlockType.TCP: [
                "ПРОВЕРЬТЕ НАСТРОЙКИ БРАНДМАУЭРА",
                "ИСПОЛЬЗУЙТЕ РЕЖИМ 'УНИВЕРС.' ИЛИ 'АГРЕССИВ'",
                "ВКЛЮЧИТЕ ВСЕ TCP-СЕРВИСЫ"
            ],
            BlockType.HTTP: [
                "ПРИНУДИТЕЛЬНО ИСПОЛЬЗУЙТЕ HTTPS",
                "ПОПРОБУЙТЕ РЕЖИМ 'СТАНДАРТ'",
                "ВКЛЮЧИТЕ ПОДДЕРЖКУ HTTP"
            ],
            BlockType.HTTPS: [
                "ИСПОЛЬЗУЙТЕ РЕЖИМ 'АГРЕССИВ' С TLS-ФРАГМЕНТАЦИЕЙ",
                "ПОПРОБУЙТЕ РЕЖИМ 'УЛЬТРА'",
                "ВКЛЮЧИТЕ ВСЕ СЕРВИСЫ"
            ],
            BlockType.TLS: [
                "ИСПОЛЬЗУЙТЕ РЕЖИМ 'УЛЬТРА' ИЛИ 'ЭКСТРИМ'",
                "ВКЛЮЧИТЕ ПОДДЕРЖКУ TLS",
                "ПОПРОБУЙТЕ РАЗНЫЕ TLS ПАТТЕРНЫ"
            ],
            BlockType.TIMEOUT: [
                "ПРОВЕРЬТЕ ПОДКЛЮЧЕНИЕ К ИНТЕРНЕТУ",
                "ВОЗМОЖНА БЛОКИРОВКА ПО IP",
                "ПЕРЕЗАПУСТИТЕ ПРОГРАММУ"
            ]
        }
        
        service_specific = {
            "Instagram": "ДЛЯ INSTAGRAM ИСПОЛЬЗУЙТЕ РЕЖИМ 'АГРЕССИВ' ИЛИ 'УЛЬТРА'",
            "Facebook": "ДЛЯ FACEBOOK ИСПОЛЬЗУЙТЕ РЕЖИМ 'АГРЕССИВ'",
            "Telegram": "ДЛЯ TELEGRAM ВКЛЮЧИТЕ ПОДДЕРЖКУ UDP",
            "Discord": "ДЛЯ DISCORD ВКЛЮЧИТЕ ВСЕ UDP-ПОРТЫ",
            "TikTok": "ДЛЯ TIKTOK ИСПОЛЬЗУЙТЕ РЕЖИМ 'СТАНДАРТ'"
        }
        
        if block_type in recommendations:
            for rec in recommendations[block_type]:
                self._add_result(f"  • {rec}")
                self._add_recommendation(rec)
        
        for key, rec in service_specific.items():
            if key.lower() in service.lower():
                self._add_result(f"  • {rec}")
                self._add_recommendation(rec)
        
        # Добавляем рекомендацию использовать авто-подбор
        self._add_result("\n  • 🤖 ИСПОЛЬЗУЙТЕ КНОПКУ АВТО-ПОДБОРА ДЛЯ ОПТИМАЛЬНЫХ НАСТРОЕК")
        self._add_recommendation("ИСПОЛЬЗУЙТЕ АВТО-ПОДБОР ДЛЯ ОПТИМАЛЬНЫХ НАСТРОЕК")
    
    def _open_auto_bypass(self):
        """Открытие окна авто-подбора"""
        if self.last_diagnostics_data:
            AutoBypassWindow(self, self.last_diagnostics_data, self.log)


class PacketWindow(ctk.CTkToplevel, NeonBaseWindow):
    """Окно настроек пакетов в неоновом стиле"""
    
    def __init__(self, parent, process_manager: ProcessManager, config: ConfigManager, log_callback):
        super().__init__(parent)
        NeonBaseWindow.__init__(self, self)
        
        self.process_manager = process_manager
        self.config = config
        self.log = log_callback
        self.bypass_manager = BypassMethodManager()
        
        self.title("⚡ GLOBAL-ZAPRET-PRO :: НАСТРОЙКИ ПАКЕТОВ ⚡")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        self._create_neon_header(self, "РАСШИРЕННЫЕ НАСТРОЙКИ", f"ДОСТУПНО {self.bypass_manager.get_methods_count()} МЕТОДОВ")
        
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=NEON_THEME['bg_secondary'],
            border_width=2,
            border_color=NEON_THEME['primary'],
            corner_radius=8,
            scrollbar_button_color=NEON_THEME['primary'],
            scrollbar_button_hover_color=NEON_THEME['secondary']
        )
        container.pack(pady=8, padx=12, fill="both", expand=True)
        
        ports_frame = ctk.CTkFrame(container, fg_color="transparent")
        ports_frame.pack(pady=4, padx=8, fill="x")
        
        ports_label = ctk.CTkLabel(
            ports_frame,
            text="🔌 ПОРТЫ",
            font=("Courier New", 14, "bold"),
            text_color=NEON_THEME['primary']
        )
        ports_label.pack(anchor="w", pady=(0, 8))
        
        tcp_frame = ctk.CTkFrame(ports_frame, fg_color="transparent")
        tcp_frame.pack(fill="x", pady=4)
        
        tcp_label = ctk.CTkLabel(
            tcp_frame,
            text="TCP:",
            font=("Courier New", 11, "bold"),
            width=50,
            text_color=NEON_THEME['text_primary']
        )
        tcp_label.pack(side="left")
        
        self.tcp_entry = ctk.CTkEntry(
            tcp_frame,
            placeholder_text=TCP_PORTS,
            font=("Courier New", 10),
            height=30,
            fg_color=NEON_THEME['bg_tertiary'],
            border_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary']
        )
        self.tcp_entry.insert(0, self.process_manager.packet_config.tcp_ports)
        self.tcp_entry.pack(side="left", fill="x", expand=True, padx=(4, 0))
        
        udp_frame = ctk.CTkFrame(ports_frame, fg_color="transparent")
        udp_frame.pack(fill="x", pady=4)
        
        udp_label = ctk.CTkLabel(
            udp_frame,
            text="UDP:",
            font=("Courier New", 11, "bold"),
            width=50,
            text_color=NEON_THEME['text_primary']
        )
        udp_label.pack(side="left")
        
        self.udp_entry = ctk.CTkEntry(
            udp_frame,
            placeholder_text=UDP_PORTS,
            font=("Courier New", 10),
            height=30,
            fg_color=NEON_THEME['bg_tertiary'],
            border_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary']
        )
        self.udp_entry.insert(0, self.process_manager.packet_config.udp_ports)
        self.udp_entry.pack(side="left", fill="x", expand=True, padx=(4, 0))
        
        game_frame = ctk.CTkFrame(ports_frame, fg_color="transparent")
        game_frame.pack(fill="x", pady=4)
        
        game_label = ctk.CTkLabel(
            game_frame,
            text="GAME:",
            font=("Courier New", 11, "bold"),
            width=50,
            text_color=NEON_THEME['text_primary']
        )
        game_label.pack(side="left")
        
        self.game_entry = ctk.CTkEntry(
            game_frame,
            placeholder_text="27015,27016",
            font=("Courier New", 10),
            height=30,
            fg_color=NEON_THEME['bg_tertiary'],
            border_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary']
        )
        self.game_entry.insert(0, getattr(self.process_manager.packet_config, 'game_filter', ''))
        self.game_entry.pack(side="left", fill="x", expand=True, padx=(4, 4))
        
        load_gf_btn = ctk.CTkButton(
            game_frame,
            text="📂",
            command=self._load_game_filter_file,
            height=30,
            width=40,
            corner_radius=4,
            fg_color=NEON_THEME['success'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 12, "bold")
        )
        load_gf_btn.pack(side="left")
        
        separator1 = ctk.CTkFrame(ports_frame, height=1, fg_color=NEON_THEME['primary'])
        separator1.pack(pady=8, fill="x")
        
        params_frame = ctk.CTkFrame(container, fg_color="transparent")
        params_frame.pack(pady=4, padx=8, fill="x")
        
        params_label = ctk.CTkLabel(
            params_frame,
            text="⚙ ПАРАМЕТРЫ ПАКЕТОВ",
            font=("Courier New", 14, "bold"),
            text_color=NEON_THEME['primary']
        )
        params_label.pack(anchor="w", pady=(0, 8))
        
        split_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        split_frame.pack(fill="x", pady=4)
        
        split_label_title = ctk.CTkLabel(
            split_frame,
            text="SPLIT POS:",
            font=("Courier New", 11, "bold"),
            width=80,
            text_color=NEON_THEME['text_primary']
        )
        split_label_title.pack(side="left")
        
        self.split_var = ctk.IntVar(value=self.process_manager.packet_config.split_pos)
        split_slider = ctk.CTkSlider(
            split_frame,
            from_=1, to=10,
            number_of_steps=9,
            variable=self.split_var,
            command=self._update_split_label,
            height=14,
            width=180,
            fg_color=NEON_THEME['bg_tertiary'],
            progress_color=NEON_THEME['primary'],
            button_color=NEON_THEME['primary'],
            button_hover_color=NEON_THEME['secondary']
        )
        split_slider.pack(side="left", padx=(4, 8))
        
        self.split_label = ctk.CTkLabel(
            split_frame,
            text=str(self.split_var.get()),
            width=30,
            font=("Courier New", 12, "bold"),
            text_color=NEON_THEME['primary']
        )
        self.split_label.pack(side="left")
        
        frag_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        frag_frame.pack(fill="x", pady=4)
        
        frag_label_title = ctk.CTkLabel(
            frag_frame,
            text="FRAG SIZE:",
            font=("Courier New", 11, "bold"),
            width=80,
            text_color=NEON_THEME['text_primary']
        )
        frag_label_title.pack(side="left")
        
        self.frag_var = ctk.IntVar(value=self.process_manager.packet_config.fragment_size)
        frag_slider = ctk.CTkSlider(
            frag_frame,
            from_=32, to=512,
            number_of_steps=15,
            variable=self.frag_var,
            command=self._update_frag_label,
            height=14,
            width=180,
            fg_color=NEON_THEME['bg_tertiary'],
            progress_color=NEON_THEME['primary'],
            button_color=NEON_THEME['primary'],
            button_hover_color=NEON_THEME['secondary']
        )
        frag_slider.pack(side="left", padx=(4, 8))
        
        self.frag_label = ctk.CTkLabel(
            frag_frame,
            text=str(self.frag_var.get()),
            width=30,
            font=("Courier New", 12, "bold"),
            text_color=NEON_THEME['primary']
        )
        self.frag_label.pack(side="left")
        
        ttl_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        ttl_frame.pack(fill="x", pady=4)
        
        ttl_label_title = ctk.CTkLabel(
            ttl_frame,
            text="TTL RANGE:",
            font=("Courier New", 11, "bold"),
            width=80,
            text_color=NEON_THEME['text_primary']
        )
        ttl_label_title.pack(side="left")
        
        ttl_range_frame = ctk.CTkFrame(ttl_frame, fg_color="transparent")
        ttl_range_frame.pack(side="left", fill="x", expand=True)
        
        self.ttl_min_var = ctk.IntVar(value=self.process_manager.packet_config.ttl_min)
        ttl_min_entry = ctk.CTkEntry(
            ttl_range_frame,
            textvariable=self.ttl_min_var,
            width=50,
            height=30,
            font=("Courier New", 10),
            fg_color=NEON_THEME['bg_tertiary'],
            border_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary']
        )
        ttl_min_entry.pack(side="left")
        
        ttl_sep = ctk.CTkLabel(
            ttl_range_frame,
            text="—",
            font=("Courier New", 14, "bold"),
            width=15,
            text_color=NEON_THEME['primary']
        )
        ttl_sep.pack(side="left")
        
        self.ttl_max_var = ctk.IntVar(value=self.process_manager.packet_config.ttl_max)
        ttl_max_entry = ctk.CTkEntry(
            ttl_range_frame,
            textvariable=self.ttl_max_var,
            width=50,
            height=30,
            font=("Courier New", 10),
            fg_color=NEON_THEME['bg_tertiary'],
            border_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary']
        )
        ttl_max_entry.pack(side="left")
        
        win_frame = ctk.CTkFrame(params_frame, fg_color="transparent")
        win_frame.pack(fill="x", pady=4)
        
        win_label_title = ctk.CTkLabel(
            win_frame,
            text="WINDOW:",
            font=("Courier New", 11, "bold"),
            width=80,
            text_color=NEON_THEME['text_primary']
        )
        win_label_title.pack(side="left")
        
        self.win_var = ctk.IntVar(value=self.process_manager.packet_config.window_size)
        win_slider = ctk.CTkSlider(
            win_frame,
            from_=4096, to=131070,
            number_of_steps=20,
            variable=self.win_var,
            command=self._update_win_label,
            height=14,
            width=180,
            fg_color=NEON_THEME['bg_tertiary'],
            progress_color=NEON_THEME['primary'],
            button_color=NEON_THEME['primary'],
            button_hover_color=NEON_THEME['secondary']
        )
        win_slider.pack(side="left", padx=(4, 8))
        
        self.win_label = ctk.CTkLabel(
            win_frame,
            text=str(self.win_var.get()),
            width=50,
            font=("Courier New", 10),
            text_color=NEON_THEME['primary']
        )
        self.win_label.pack(side="left")
        
        separator2 = ctk.CTkFrame(params_frame, height=1, fg_color=NEON_THEME['primary'])
        separator2.pack(pady=8, fill="x")
        
        method_frame = ctk.CTkFrame(container, fg_color="transparent")
        method_frame.pack(pady=4, padx=8, fill="x")
        
        method_label = ctk.CTkLabel(
            method_frame,
            text="🎭 ВЫБОР МЕТОДА ОБХОДА",
            font=("Courier New", 14, "bold"),
            text_color=NEON_THEME['primary']
        )
        method_label.pack(anchor="w", pady=(0, 8))
        
        method_select_frame = ctk.CTkFrame(method_frame, fg_color="transparent")
        method_select_frame.pack(fill="x", pady=4)
        
        method_select_label = ctk.CTkLabel(
            method_select_frame,
            text="МЕТОД:",
            font=("Courier New", 11, "bold"),
            width=70,
            text_color=NEON_THEME['text_primary']
        )
        method_select_label.pack(side="left")
        
        current_method = self.process_manager.packet_config.custom_methods
        current_display = "Экстрим (все методы)"
        
        all_method_displays = self.bypass_manager.get_all_method_values()
        for display in all_method_displays:
            method_value = self.bypass_manager.get_method_by_display(display)
            if method_value == current_method:
                current_display = display
                break
        
        self.method_var = ctk.StringVar(value=current_display)
        method_menu = ctk.CTkOptionMenu(
            method_select_frame,
            values=all_method_displays,
            variable=self.method_var,
            font=("Courier New", 10),
            height=30,
            width=400,
            fg_color=NEON_THEME['bg_tertiary'],
            button_color=NEON_THEME['primary'],
            button_hover_color=NEON_THEME['secondary'],
            dropdown_fg_color=NEON_THEME['bg_secondary'],
            dropdown_hover_color=NEON_THEME['bg_tertiary'],
            text_color=NEON_THEME['text_primary']
        )
        method_menu.pack(side="left", fill="x", expand=True, padx=(4, 0))
        
        method_menu.bind("<MouseWheel>", self._on_mousewheel)
        
        method_info = ctk.CTkLabel(
            method_frame,
            text=f"🔧 ИСПОЛЬЗУЙТЕ КОЛЕСИКО МЫШИ ДЛЯ ПРОКРУТКИ ({self.bypass_manager.get_methods_count()} МЕТОДОВ)",
            font=("Courier New", 9),
            text_color=NEON_THEME['text_dim']
        )
        method_info.pack(anchor="w", padx=(80, 0), pady=(4, 8))
        
        separator3 = ctk.CTkFrame(method_frame, height=1, fg_color=NEON_THEME['primary'])
        separator3.pack(pady=4, fill="x")
        
        fooling_frame = ctk.CTkFrame(container, fg_color="transparent")
        fooling_frame.pack(pady=4, padx=8, fill="x")
        
        fooling_label = ctk.CTkLabel(
            fooling_frame,
            text="🎭 МЕТОДЫ ОБМАНА",
            font=("Courier New", 14, "bold"),
            text_color=NEON_THEME['primary']
        )
        fooling_label.pack(anchor="w", pady=(0, 8))
        
        fooling_select = ctk.CTkFrame(fooling_frame, fg_color="transparent")
        fooling_select.pack(fill="x", pady=4)
        
        fooling_select_label = ctk.CTkLabel(
            fooling_select,
            text="ТИП:",
            font=("Courier New", 11, "bold"),
            width=70,
            text_color=NEON_THEME['text_primary']
        )
        fooling_select_label.pack(side="left")
        
        self.fooling_var = ctk.StringVar(value=self.process_manager.packet_config.fooling)
        fooling_menu = ctk.CTkOptionMenu(
            fooling_select,
            values=["ts", "md5", "md5sig", "badsum", "none", "random"],
            variable=self.fooling_var,
            font=("Courier New", 11),
            height=30,
            fg_color=NEON_THEME['bg_tertiary'],
            button_color=NEON_THEME['primary'],
            button_hover_color=NEON_THEME['secondary'],
            dropdown_fg_color=NEON_THEME['bg_secondary'],
            dropdown_hover_color=NEON_THEME['bg_tertiary'],
            text_color=NEON_THEME['text_primary']
        )
        fooling_menu.pack(side="left", fill="x", expand=True, padx=(4, 0))
        
        checks_frame = ctk.CTkFrame(fooling_frame, fg_color="transparent")
        checks_frame.pack(fill="x", pady=8)
        
        row1 = ctk.CTkFrame(checks_frame, fg_color="transparent")
        row1.pack(fill="x", pady=2)
        
        self.randomize_var = ctk.BooleanVar(value=self.process_manager.packet_config.randomize)
        randomize_check = ctk.CTkCheckBox(
            row1,
            text="РАНДОМИЗАЦИЯ TTL/WINDOW",
            variable=self.randomize_var,
            font=("Courier New", 10),
            fg_color=NEON_THEME['primary'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['text_primary'],
            border_color=NEON_THEME['primary'],
            checkbox_width=18,
            checkbox_height=18
        )
        randomize_check.pack(side="left", padx=2, expand=True, fill="x")
        
        self.auto_restart_var = ctk.BooleanVar(value=self.process_manager.packet_config.auto_restart)
        auto_restart_check = ctk.CTkCheckBox(
            row1,
            text="АВТОПЕРЕЗАПУСК",
            variable=self.auto_restart_var,
            font=("Courier New", 10),
            fg_color=NEON_THEME['primary'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['text_primary'],
            border_color=NEON_THEME['primary'],
            checkbox_width=18,
            checkbox_height=18
        )
        auto_restart_check.pack(side="left", padx=2, expand=True, fill="x")
        
        row2 = ctk.CTkFrame(checks_frame, fg_color="transparent")
        row2.pack(fill="x", pady=2)
        
        self.use_proxy_var = ctk.BooleanVar(value=self.process_manager.packet_config.use_proxy)
        use_proxy_check = ctk.CTkCheckBox(
            row2,
            text="ИСПОЛЬЗОВАТЬ ПРОКСИ",
            variable=self.use_proxy_var,
            font=("Courier New", 10),
            fg_color=NEON_THEME['primary'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['text_primary'],
            border_color=NEON_THEME['primary'],
            checkbox_width=18,
            checkbox_height=18
        )
        use_proxy_check.pack(side="left", padx=2, expand=True, fill="x")
        
        proxy_frame = ctk.CTkFrame(fooling_frame, fg_color="transparent")
        proxy_frame.pack(fill="x", pady=4)
        
        proxy_label = ctk.CTkLabel(
            proxy_frame,
            text="ПРОКСИ:",
            font=("Courier New", 11, "bold"),
            width=70,
            text_color=NEON_THEME['text_primary']
        )
        proxy_label.pack(side="left")
        
        self.proxy_entry = ctk.CTkEntry(
            proxy_frame,
            placeholder_text="socks5://127.0.0.1:1080",
            font=("Courier New", 10),
            height=30,
            fg_color=NEON_THEME['bg_tertiary'],
            border_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary']
        )
        self.proxy_entry.insert(0, self.process_manager.packet_config.proxy_address)
        self.proxy_entry.pack(side="left", fill="x", expand=True, padx=(4, 0))
        
        separator4 = ctk.CTkFrame(fooling_frame, height=1, fg_color=NEON_THEME['primary'])
        separator4.pack(pady=8, fill="x")
        
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=15, fill="x", padx=25)
        
        apply_btn = ctk.CTkButton(
            btn_frame,
            text="✅ ПРИМЕНИТЬ НАСТРОЙКИ",
            command=self._apply_settings,
            height=40,
            corner_radius=8,
            fg_color=NEON_THEME['success'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 13, "bold")
        )
        apply_btn.pack(pady=4, fill="x")
        
        reset_btn = ctk.CTkButton(
            btn_frame,
            text="🔄 СБРОСИТЬ К УМОЛЧАНИЮ",
            command=self._reset_defaults,
            height=35,
            corner_radius=8,
            fg_color=NEON_THEME['warning'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 12, "bold")
        )
        reset_btn.pack(pady=4, fill="x")
    
    def _on_mousewheel(self, event):
        try:
            current_values = self.method_var.get()
            all_values = self.bypass_manager.get_all_method_values()
            
            try:
                current_index = all_values.index(current_values)
            except ValueError:
                current_index = 0
            
            if event.delta > 0:
                new_index = (current_index - 1) % len(all_values)
            else:
                new_index = (current_index + 1) % len(all_values)
            
            self.method_var.set(all_values[new_index])
        except:
            pass
    
    def _load_game_filter_file(self):
        svc = ServiceManager(self.config.base_path, self.log)
        gf = svc.load_game_filter()
        if gf:
            self.game_entry.delete(0, "end")
            self.game_entry.insert(0, gf)
            self.log(f"[GAME_FILTER] ЗАГРУЖЕНО: {gf[:60]}")
        else:
            self.log("[GAME_FILTER] ФАЙЛ НЕ НАЙДЕН")
    
    def _update_split_label(self, value):
        self.split_label.configure(text=str(int(value)))
    
    def _update_frag_label(self, value):
        self.frag_label.configure(text=str(int(value)))
    
    def _update_win_label(self, value):
        self.win_label.configure(text=str(int(value)))
    
    def _apply_settings(self):
        try:
            method_display = self.method_var.get()
            method_value = self.bypass_manager.get_method_by_display(method_display)
            
            new_config = PacketConfig(
                tcp_ports=self.tcp_entry.get().strip(),
                udp_ports=self.udp_entry.get().strip(),
                split_pos=self.split_var.get(),
                fooling=self.fooling_var.get(),
                auto_restart=self.auto_restart_var.get(),
                fragment_size=self.frag_var.get(),
                ttl_min=self.ttl_min_var.get(),
                ttl_max=self.ttl_max_var.get(),
                window_size=self.win_var.get(),
                randomize=self.randomize_var.get(),
                use_proxy=self.use_proxy_var.get(),
                proxy_address=self.proxy_entry.get().strip(),
                custom_methods=method_value
            )
            new_config.game_filter = self.game_entry.get().strip()
            
            self.process_manager.update_packet_config(new_config)
            self.log("[ПАКЕТЫ] НАСТРОЙКИ ПРИМЕНЕНЫ")
            self.log(f"[ПАКЕТЫ] МЕТОД: {method_display}")
            self.log(f"[ПАКЕТЫ] FOOLING: {new_config.fooling}")
            
            if new_config.auto_restart:
                self.log("[ПАКЕТЫ] ПЕРЕЗАПУСК DPI...")
            
            self.destroy()
            
        except Exception as e:
            self.log(f"[ОШИБКА] {e}")
    
    def _reset_defaults(self):
        self.tcp_entry.delete(0, "end")
        self.tcp_entry.insert(0, TCP_PORTS)
        
        self.udp_entry.delete(0, "end")
        self.udp_entry.insert(0, UDP_PORTS)
        
        self.game_entry.delete(0, "end")
        
        self.split_var.set(1)
        self._update_split_label(1)
        
        self.frag_var.set(128)
        self._update_frag_label(128)
        
        self.ttl_min_var.set(32)
        self.ttl_max_var.set(128)
        
        self.win_var.set(65535)
        self._update_win_label(65535)
        
        default_method = "fake,multisplit,disorder2,hole,fragment,badsum"
        for display in self.bypass_manager.get_all_method_values():
            if self.bypass_manager.get_method_by_display(display) == default_method:
                self.method_var.set(display)
                break
        
        self.fooling_var.set("ts")
        self.randomize_var.set(False)
        self.auto_restart_var.set(True)
        self.use_proxy_var.set(False)
        
        self.proxy_entry.delete(0, "end")
        self.proxy_entry.insert(0, "socks5://127.0.0.1:1080")
        
        self.log("[ПАКЕТЫ] СБРОС К УМОЛЧАНИЮ")


class ServicesWindow(ctk.CTkToplevel, NeonBaseWindow):
    """Окно настроек сервисов в неоновом стиле"""
    
    def __init__(self, parent, process_manager: ProcessManager, config: ConfigManager, log_callback):
        super().__init__(parent)
        NeonBaseWindow.__init__(self, self)
        
        self.process_manager = process_manager
        self.config = config
        self.log = log_callback
        self.parent = parent
        
        self.title("⚡ GLOBAL-ZAPRET-PRO :: УПРАВЛЕНИЕ СЕРВИСАМИ ⚡")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        self._create_neon_header(self, "УПРАВЛЕНИЕ СЕРВИСАМИ", "ВЫБЕРИТЕ ЦЕЛЕВЫЕ СЕРВИСЫ")
        
        container = ctk.CTkScrollableFrame(
            self,
            fg_color=NEON_THEME['bg_secondary'],
            border_width=2,
            border_color=NEON_THEME['primary'],
            corner_radius=8,
            scrollbar_button_color=NEON_THEME['primary'],
            scrollbar_button_hover_color=NEON_THEME['secondary']
        )
        container.pack(pady=12, padx=12, fill="both", expand=True)
        
        self._create_service_controls(container)
        self._create_action_buttons()
    
    def _create_service_controls(self, parent):
        services = [
            ("general", "🌐 ОБЩИЙ (ВСЕ САЙТЫ)", NEON_THEME['primary']),
            ("google", "🔍 GOOGLE", "#4285f4"),
            ("meta", "📸 META (IG/FB)", "#1877f2"),
            ("x", "🐦 X.COM / TWITTER", NEON_THEME['text_primary']),
            ("tiktok", "📱 TIKTOK", "#ff0050"),
            ("telegram", "✈️ TELEGRAM", "#26a5e4"),
            ("discord", "🎮 DISCORD", NEON_THEME['primary']),
            ("games", "🎲 ИГРЫ", NEON_THEME['success']),
            ("mylist", "📋 ПОЛЬЗОВАТЕЛЬСКИЙ", NEON_THEME['warning'])
        ]
        
        self.service_vars = {}
        
        for i, (service_id, display_name, color) in enumerate(services):
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            frame.pack(fill="x", padx=12, pady=6)
            
            enabled = self.process_manager.service_configs[service_id].enabled
            
            var = ctk.BooleanVar(value=enabled)
            self.service_vars[service_id] = var
            
            check = ctk.CTkCheckBox(
                frame,
                text=display_name,
                variable=var,
                command=lambda sid=service_id: self._toggle_service(sid),
                font=("Courier New", 12),
                text_color=color,
                fg_color=NEON_THEME['primary'],
                hover_color=NEON_THEME['secondary'],
                border_color=NEON_THEME['primary'],
                checkbox_width=18,
                checkbox_height=18
            )
            check.pack(side="left", padx=4)
            
            if service_id == "discord":
                info = ctk.CTkLabel(
                    frame,
                    text="[ГОЛОС]",
                    font=("Courier New", 8),
                    text_color=NEON_THEME['text_dim']
                )
                info.pack(side="left", padx=(10, 0))
            elif service_id == "general":
                info = ctk.CTkLabel(
                    frame,
                    text="[БАЗА]",
                    font=("Courier New", 8),
                    text_color=NEON_THEME['text_dim']
                )
                info.pack(side="left", padx=(10, 0))
        
        separator = ctk.CTkFrame(parent, height=1, fg_color=NEON_THEME['primary'])
        separator.pack(padx=12, pady=12, fill="x")
        
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(padx=12, pady=8, fill="x")
        
        select_all = ctk.CTkButton(
            btn_frame,
            text="✅ ВЫБРАТЬ ВСЕ",
            command=self._select_all,
            height=30,
            corner_radius=6,
            fg_color=NEON_THEME['bg_tertiary'],
            hover_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary'],
            font=("Courier New", 11, "bold")
        )
        select_all.pack(side="left", padx=4, expand=True, fill="x")
        
        deselect_all = ctk.CTkButton(
            btn_frame,
            text="❌ ОТКЛЮЧИТЬ ВСЕ",
            command=self._deselect_all,
            height=30,
            corner_radius=6,
            fg_color=NEON_THEME['bg_tertiary'],
            hover_color=NEON_THEME['error'],
            text_color=NEON_THEME['text_primary'],
            font=("Courier New", 11, "bold")
        )
        deselect_all.pack(side="right", padx=4, expand=True, fill="x")
    
    def _create_action_buttons(self):
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=(0, 15), fill="x", padx=25)
        
        row1 = ctk.CTkFrame(button_frame, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 4))
        
        packets_btn = ctk.CTkButton(
            row1,
            text="📦 НАСТРОЙКИ ПАКЕТОВ",
            command=self._open_packets,
            height=35,
            corner_radius=8,
            fg_color=NEON_THEME['warning'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 12, "bold")
        )
        packets_btn.pack(side="left", padx=(0, 4), expand=True, fill="x")
        
        diag_btn = ctk.CTkButton(
            row1,
            text="🔍 ДИАГНОСТИКА",
            command=self._open_diagnostics,
            height=35,
            corner_radius=8,
            fg_color=NEON_THEME['info'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 12, "bold")
        )
        diag_btn.pack(side="right", padx=(4, 0), expand=True, fill="x")
    
    def _open_packets(self):
        PacketWindow(self, self.process_manager, self.config, self.log)
    
    def _open_diagnostics(self):
        DiagnosticsWindow(self, self.log)
    
    def _toggle_service(self, service_id: str):
        enabled = self.service_vars[service_id].get()
        
        threading.Thread(
            target=lambda: self.process_manager.set_service_enabled(service_id, enabled),
            daemon=True
        ).start()
        
        service_names = {
            "general": "ОБЩИЙ", "google": "GOOGLE", "meta": "META",
            "x": "X.COM", "tiktok": "TIKTOK", "telegram": "TELEGRAM",
            "discord": "DISCORD", "games": "ИГРЫ", "mylist": "МОЙ СПИСОК"
        }
        
        name = service_names.get(service_id, service_id.upper())
        self.log(f"[{name}] ОБХОД {'ВКЛЮЧЕН' if enabled else 'ОТКЛЮЧЕН'}")
        
        services_config = self.config.get("services", {})
        if service_id not in services_config:
            services_config[service_id] = {}
        services_config[service_id]["enabled"] = enabled
        self.config.set("services", services_config)
    
    def _select_all(self):
        for service_id, var in self.service_vars.items():
            var.set(True)
            self._toggle_service(service_id)
        self.log("[ВСЕ] ОБХОД ВКЛЮЧЕН ДЛЯ ВСЕХ СЕРВИСОВ")
    
    def _deselect_all(self):
        for service_id, var in self.service_vars.items():
            var.set(False)
            self._toggle_service(service_id)
        self.log("[ВСЕ] ОБХОД ОТКЛЮЧЕН ДЛЯ ВСЕХ СЕРВИСОВ")


class AutostartWindow(ctk.CTkToplevel, NeonBaseWindow):
    """Окно автозапуска в неоновом стиле"""
    
    def __init__(self, parent, config: ConfigManager, log_callback):
        super().__init__(parent)
        NeonBaseWindow.__init__(self, self)
        
        self.config = config
        self.log = log_callback
        
        self.title("⚡ GLOBAL-ZAPRET-PRO :: АВТОЗАПУСК ⚡")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        self._create_neon_header(self, "НАСТРОЙКИ ЗАПУСКА", "КОНФИГУРАЦИЯ АВТОМАТИЧЕСКОГО ЗАПУСКА")
        
        frame = ctk.CTkFrame(
            self, 
            fg_color=NEON_THEME['bg_secondary'], 
            border_width=2, 
            border_color=NEON_THEME['primary'], 
            corner_radius=8
        )
        frame.pack(pady=25, padx=25, fill="both", expand=True)
        
        self.autostart_var = ctk.BooleanVar(value=self.config.get("autostart", False))
        autostart_check = ctk.CTkCheckBox(
            frame,
            text="АВТОЗАГРУЗКА ПРИ СТАРТЕ WINDOWS",
            variable=self.autostart_var,
            command=self._toggle_autostart,
            font=("Courier New", 13),
            fg_color=NEON_THEME['primary'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['text_primary'],
            border_color=NEON_THEME['primary'],
            checkbox_width=20,
            checkbox_height=20
        )
        autostart_check.pack(pady=25, padx=25, anchor="w")
        
        separator = ctk.CTkFrame(frame, height=1, fg_color=NEON_THEME['primary'])
        separator.pack(pady=15, padx=25, fill="x")
        
        self.auto_run_var = ctk.BooleanVar(value=self.config.get("auto_run", True))
        auto_run_check = ctk.CTkCheckBox(
            frame,
            text="АВТОМАТИЧЕСКИЙ ЗАПУСК DPI",
            variable=self.auto_run_var,
            command=self._toggle_auto_run,
            font=("Courier New", 13),
            fg_color=NEON_THEME['primary'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['text_primary'],
            border_color=NEON_THEME['primary'],
            checkbox_width=20,
            checkbox_height=20
        )
        auto_run_check.pack(pady=25, padx=25, anchor="w")
        
        self.start_minimized_var = ctk.BooleanVar(value=self.config.get("start_minimized", True))
        start_minimized_check = ctk.CTkCheckBox(
            frame,
            text="ЗАПУСК В СИСТЕМНЫЙ ТРЕЙ",
            variable=self.start_minimized_var,
            command=self._toggle_start_minimized,
            font=("Courier New", 13),
            fg_color=NEON_THEME['primary'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['text_primary'],
            border_color=NEON_THEME['primary'],
            checkbox_width=20,
            checkbox_height=20
        )
        start_minimized_check.pack(pady=25, padx=25, anchor="w")
    
    def _toggle_autostart(self):
        enabled = self.autostart_var.get()
        self.config.set("autostart", enabled)
        
        try:
            import winreg
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            if enabled:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                if getattr(sys, 'frozen', False):
                    executable = sys.executable
                else:
                    executable = f'"{sys.executable}" "{sys.argv[0]}"'
                winreg.SetValueEx(key, "Global-Zapret-Pro", 0, winreg.REG_SZ, executable)
                winreg.CloseKey(key)
                self.log("[АВТОЗАПУСК] ДОБАВЛЕН В АВТОЗАГРУЗКУ")
            else:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
                    winreg.DeleteValue(key, "Global-Zapret-Pro")
                    winreg.CloseKey(key)
                    self.log("[АВТОЗАПУСК] УДАЛЕН ИЗ АВТОЗАГРУЗКИ")
                except:
                    pass
        except Exception as e:
            self.log(f"[ОШИБКА] АВТОЗАПУСК: {e}")
    
    def _toggle_auto_run(self):
        enabled = self.auto_run_var.get()
        self.config.set("auto_run", enabled)
        self.log(f"[АВТОЗАПУСК DPI] {'ВКЛЮЧЕН' if enabled else 'ОТКЛЮЧЕН'}")
    
    def _toggle_start_minimized(self):
        enabled = self.start_minimized_var.get()
        self.config.set("start_minimized", enabled)
        self.log(f"[ЗАПУСК В ТРЕЙ] {'ВКЛЮЧЕН' if enabled else 'ОТКЛЮЧЕН'}")


class HelpWindow(ctk.CTkToplevel, NeonBaseWindow):
    """Окно справки в неоновом стиле"""
    
    def __init__(self, parent):
        super().__init__(parent)
        NeonBaseWindow.__init__(self, self)
        
        self.title("⚡ GLOBAL-ZAPRET-PRO :: СПРАВКА ⚡")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self._setup_ui()
    
    def _setup_ui(self):
        self._create_neon_header(self, "РУКОВОДСТВО ПОЛЬЗОВАТЕЛЯ", "ВСЯ НЕОБХОДИМАЯ ИНФОРМАЦИЯ")
        
        text_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=NEON_THEME['bg_secondary'],
            border_width=2,
            border_color=NEON_THEME['primary'],
            corner_radius=8,
            scrollbar_button_color=NEON_THEME['primary'],
            scrollbar_button_hover_color=NEON_THEME['secondary']
        )
        text_frame.pack(pady=12, padx=15, fill="both", expand=True)
        
        bypass_manager = BypassMethodManager()
        methods_count = bypass_manager.get_methods_count()
        
        help_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║              GLOBAL-ZAPRET-PRO v5.2.0 ULTIMATE                   ║
║                     НЕОНОВАЯ ВЕРСИЯ                              ║
╚══════════════════════════════════════════════════════════════════╝

>> БЫСТРЫЙ СТАРТ <<
──────────────────────────────────────────────────────────────────
• ЗАПУСКАЙТЕ ОТ ИМЕНИ АДМИНИСТРАТОРА
• DPI ОБХОД АКТИВИРУЕТСЯ АВТОМАТИЧЕСКИ
• ИКОНКА ПОЯВИТСЯ В СИСТЕМНОМ ТРЕЕ

>> ДОСТУПНЫЕ МЕТОДЫ ОБХОДА ({methods_count}) <<
──────────────────────────────────────────────────────────────────
БАЗОВЫЕ: fake, fake2, fake_multi
РАЗДЕЛЕНИЕ: multisplit, split, split2, split3, split4, split5
ПОРЯДОК: disorder, disorder2, disorder3, disorder4, disorder5
ФРАГМЕНТАЦИЯ: fragment, fragment2, fragment3, fragment4, fragment5
КОНТРОЛЬ: badsum, badsum2, badsum3, md5, md5sig, md5sig2, md5sig3
ДЫРЫ: hole, hole2, hole3, hole4, hole5
ПЕРЕКРЫТИЕ: seqovl, seqovl2, seqovl3, seqovl4, seqovl5, seqovl6
TCP: tcpopt, wsize, mss
TTL: ttl, ttl_random, ttl_dec, ttl_inc
PADDING: padding, padding_random
ШИФРОВАНИЕ: encrypt, mimic
ТУННЕЛИРОВАНИЕ: tunnel, proxy
ЭКСПЛОЙТЫ: heartbleed, bleed
TLS/QUIC: tls_split, quic_split
СЛУЧАЙНЫЕ: random, random_split, random_hole
МНОЖЕСТВЕННЫЕ: multi_fake, multi_split, multi_hole, multi_all
АВТОМАТИЧЕСКИЕ: auto, smart
ПРОТОКОЛЫ: tls12, tls13, quic, http, https, websocket, dns
КОМБО: fake+multisplit, fake+hole, multisplit+hole, disorder+hole
МЕГА: all_basic, all_advanced, all_extreme, all_ultimate
ПРОДВИНУТЫЕ: advanced1-10
СТЕЛС: stealth1-10
ИГРОВЫЕ: gaming1-10
ДЛЯ САЙТОВ: youtube, netflix, twitch, discord, telegram

>> РЕЖИМЫ РАБОТЫ (11) <<
──────────────────────────────────────────────────────────────────
ЛАЙТ      → fake (повторов=4)
СТАНДАРТ  → fake,multisplit (повторов=6)
АГРЕССИВ  → +disorder2 (повторов=10)
УЛЬТРА    → +hole (повторов=12)
ПРОИЗВ.   → fake (повторов=4)
УНИВЕРС.  → +split2 (повторов=8)
ИГРОВОЙ   → split2 (повторов=6)
СТЕЛС     → hole,badsum (повторов=8)
ЭКСТРИМ   → 6 методов (повторов=15)
РАНДОМ    → random_split (повторов=10)
МУЛЬТИ    → 7 методов (повторов=12)

>> СЕРВИСЫ (9) <<
──────────────────────────────────────────────────────────────────
ОБЩИЙ     - все сайты
GOOGLE    - поиск и сервисы Google
META      - Instagram/Facebook
X.COM     - Twitter/X
TIKTOK    - TikTok
TELEGRAM  - мессенджер
DISCORD   - голосовой чат
ИГРЫ      - игровой трафик
МОЙ СПИСОК - пользовательский список

>> РЕШЕНИЕ ПРОБЛЕМ <<
──────────────────────────────────────────────────────────────────
• НЕ ЗАПУСКАЕТСЯ → проверьте наличие драйверов в папке bin
• НЕ РАБОТАЕТ   → смените режим или выберите другой метод
• ОШИБКА ДОСТУПА → запустите от имени Администратора
• АВТО-ПОДБОР   → используйте кнопку в окне диагностики
"""
        
        label = ctk.CTkLabel(
            text_frame,
            text=help_text,
            font=("Courier New", 10),
            justify="left",
            text_color=NEON_THEME['text_primary']
        )
        label.pack(pady=12, padx=12)


# ==============================================================================
# ГЛАВНОЕ НЕОНОВОЕ ОКНО
# ==============================================================================

class MainApplication(ctk.CTk, NeonBaseWindow):
    """Главное окно в неоновом стиле"""
    
    def __init__(self):
        super().__init__()
        NeonBaseWindow.__init__(self, self)
        
        self.config = ConfigManager()
        self.process_manager = ProcessManager()
        self.lists_manager = ListsManager(self.config.base_path)
        self.bypass_manager = BypassMethodManager()
        self.tray_icon = None
        self._pending_logs = []
        
        self.title("⚡ GLOBAL-ZAPRET-PRO v5.2.0 ULTIMATE ⚡")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        
        self._check_lists()
        self._setup_ui()
        
        self.service_manager = ServiceManager(self.config.base_path, self._log)
        
        self.protocol("WM_DELETE_WINDOW", self._hide_window)
        
        self.after(300, self._run_startup_checks)
        
        if self.config.get("auto_run", True):
            self.after(1000, self._auto_start)
        
        if self.config.get("first_start", True):
            self.config.set("first_start", False)
            self.after(2000, self._show_welcome_message)
    
    def _check_lists(self):
        missing = []
        for list_name in ListsManager.REQUIRED_LISTS:
            if not self.lists_manager.check_list_exists(list_name):
                missing.append(list_name)
        
        if missing:
            self._log(f"[ПРЕДУПРЕЖДЕНИЕ] ОТСУТСТВУЮТ ФАЙЛЫ: {', '.join(missing)}")
            self._log("[ИНФОРМАЦИЯ] БУДУТ СОЗДАНЫ ПУСТЫЕ ФАЙЛЫ")
    
    def _show_welcome_message(self):
        methods_count = self.bypass_manager.get_methods_count()
        self._log("⚡ GLOBAL-ZAPRET-PRO v5.2.0 ULTIMATE ⚡")
        self._log(f"✅ ЗАГРУЖЕНО {methods_count} МЕТОДОВ ОБХОДА DPI")
        self._log("✅ СИСТЕМА ГОТОВА К РАБОТЕ")
        self._log("✅ ДОБАВЛЕН АВТО-ПОДБОР МЕТОДОВ ОБХОДА")
    
    def _setup_ui(self):
        self._create_neon_header(self, "GLOBAL-ZAPRET-PRO", f"ULTIMATE v5.2.0 [{self.bypass_manager.get_methods_count()} МЕТОДОВ]")
        
        status_frame = ctk.CTkFrame(
            self, 
            fg_color=NEON_THEME['bg_secondary'], 
            corner_radius=8,
            border_width=2, 
            border_color=NEON_THEME['primary']
        )
        status_frame.pack(pady=8, padx=25, fill="x")
        
        self.status_indicator = ctk.CTkLabel(
            status_frame,
            text="●",
            font=("Arial", 20),
            text_color=NEON_THEME['error']
        )
        self.status_indicator.pack(side="left", padx=(12, 4))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="ОСТАНОВЛЕН",
            font=("Courier New", 14, "bold"),
            text_color=NEON_THEME['error']
        )
        self.status_label.pack(side="left", padx=4)
        
        self.pid_label = ctk.CTkLabel(
            status_frame,
            text="НЕТ ПРОЦЕССА",
            font=("Courier New", 9),
            text_color=NEON_THEME['text_dim']
        )
        self.pid_label.pack(side="right", padx=12)
        
        mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        mode_frame.pack(pady=6, padx=25, fill="x")
        
        mode_label = ctk.CTkLabel(
            mode_frame,
            text="🎯 РЕЖИМ ОБХОДА:",
            font=("Courier New", 11),
            text_color=NEON_THEME['text_secondary']
        )
        mode_label.pack(anchor="w", padx=4, pady=(0, 6))
        
        # Кнопки режимов с правильными отступами, не выходят за границы
        row1_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        row1_frame.pack(fill="x", pady=(0, 4))
        
        modes_row1 = ["ЛАЙТ", "СТАНДАРТ", "АГРЕССИВ", "УЛЬТРА", "ПРОИЗВ."]
        
        # Используем grid для точного контроля размеров
        for i in range(5):
            row1_frame.grid_columnconfigure(i, weight=1)
        
        for i, mode_name in enumerate(modes_row1):
            btn = ctk.CTkButton(
                row1_frame,
                text=mode_name,
                command=lambda m=mode_name: self._change_mode(m),
                height=28,
                corner_radius=6,
                fg_color=NEON_THEME['bg_tertiary'],
                hover_color=NEON_THEME['primary'],
                text_color=NEON_THEME['text_primary'],
                font=("Courier New", 10, "bold")
            )
            btn.grid(row=0, column=i, padx=1, sticky="ew")
        
        row2_frame = ctk.CTkFrame(mode_frame, fg_color="transparent")
        row2_frame.pack(fill="x")
        
        modes_row2 = ["УНИВЕРС.", "ИГРОВОЙ", "СТЕЛС", "ЭКСТРИМ", "РАНДОМ", "МУЛЬТИ"]
        
        # Настраиваем 6 колонок
        for i in range(6):
            row2_frame.grid_columnconfigure(i, weight=1)
        
        for i, mode_name in enumerate(modes_row2):
            btn = ctk.CTkButton(
                row2_frame,
                text=mode_name,
                command=lambda m=mode_name: self._change_mode(m),
                height=28,
                corner_radius=6,
                fg_color=NEON_THEME['bg_tertiary'],
                hover_color=NEON_THEME['primary'],
                text_color=NEON_THEME['text_primary'],
                font=("Courier New", 10, "bold")
            )
            btn.grid(row=0, column=i, padx=1, sticky="ew")
        
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=8, padx=25, fill="x")
        
        self.btn_start = ctk.CTkButton(
            button_frame,
            text="▶ ЗАПУСТИТЬ DPI",
            command=self._start_dpi,
            height=40,
            corner_radius=8,
            fg_color=NEON_THEME['success'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 13, "bold")
        )
        self.btn_start.pack(pady=(0, 4), fill="x")
        
        self.btn_stop = ctk.CTkButton(
            button_frame,
            text="⏹ ОСТАНОВИТЬ DPI",
            command=self._stop_dpi,
            height=40,
            corner_radius=8,
            fg_color=NEON_THEME['error'],
            hover_color=NEON_THEME['secondary'],
            text_color=NEON_THEME['bg_primary'],
            font=("Courier New", 13, "bold")
        )
        self.btn_stop.pack(pady=(0, 4), fill="x")
        
        tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame.pack(pady=(0, 4), padx=25, fill="x")
        
        self.btn_services = ctk.CTkButton(
            tools_frame,
            text="⚙ СЕРВИСЫ",
            command=self._open_services,
            height=33,
            corner_radius=6,
            fg_color=NEON_THEME['bg_tertiary'],
            hover_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary'],
            font=("Courier New", 11, "bold")
        )
        self.btn_services.pack(side="left", padx=(0, 4), expand=True, fill="x")
        
        self.btn_autostart = ctk.CTkButton(
            tools_frame,
            text="🔄 АВТОЗАПУСК",
            command=self._open_autostart,
            height=33,
            corner_radius=6,
            fg_color=NEON_THEME['bg_tertiary'],
            hover_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary'],
            font=("Courier New", 11, "bold")
        )
        self.btn_autostart.pack(side="left", padx=4, expand=True, fill="x")
        
        self.btn_help = ctk.CTkButton(
            tools_frame,
            text="📚 СПРАВКА",
            command=self._open_help,
            height=33,
            corner_radius=6,
            fg_color=NEON_THEME['bg_tertiary'],
            hover_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary'],
            font=("Courier New", 11, "bold")
        )
        self.btn_help.pack(side="left", padx=4, expand=True, fill="x")
        
        service_frame = ctk.CTkFrame(self, fg_color="transparent")
        service_frame.pack(pady=(0, 4), padx=25, fill="x")
        
        self.btn_status_check = ctk.CTkButton(
            service_frame,
            text="🔍 СТАТУС",
            command=self._check_status_zapret_btn,
            height=30,
            corner_radius=6,
            fg_color=NEON_THEME['bg_tertiary'],
            hover_color=NEON_THEME['info'],
            text_color=NEON_THEME['text_primary'],
            font=("Courier New", 10, "bold")
        )
        self.btn_status_check.pack(side="left", padx=(0, 4), expand=True, fill="x")
        
        self.btn_updates = ctk.CTkButton(
            service_frame,
            text="📡 ОБНОВЛЕНИЯ",
            command=self._check_updates_btn,
            height=30,
            corner_radius=6,
            fg_color=NEON_THEME['bg_tertiary'],
            hover_color=NEON_THEME['primary'],
            text_color=NEON_THEME['text_primary'],
            font=("Courier New", 10, "bold")
        )
        self.btn_updates.pack(side="left", padx=4, expand=True, fill="x")
        
        self.btn_game_filter = ctk.CTkButton(
            service_frame,
            text="🎮 GAME FILTER",
            command=self._load_game_filter_btn,
            height=30,
            corner_radius=6,
            fg_color=NEON_THEME['bg_tertiary'],
            hover_color=NEON_THEME['success'],
            text_color=NEON_THEME['text_primary'],
            font=("Courier New", 10, "bold")
        )
        self.btn_game_filter.pack(side="left", padx=4, expand=True, fill="x")
        
        log_label = ctk.CTkLabel(
            self,
            text="📋 ЖУРНАЛ СОБЫТИЙ",
            font=("Courier New", 12, "bold"),
            text_color=NEON_THEME['primary']
        )
        log_label.pack(pady=(6, 2))
        
        self.log_text = ctk.CTkTextbox(
            self,
            height=100,
            font=("Courier New", 10),
            fg_color=NEON_THEME['bg_secondary'],
            border_color=NEON_THEME['primary'],
            border_width=2,
            text_color=NEON_THEME['text_primary']
        )
        self.log_text.pack(pady=2, padx=25, fill="both", expand=True)
        
        footer = ctk.CTkLabel(
            self,
            text="⚡ GLOBAL-ZAPRET-PRO v5.2.0 ULTIMATE :: КОМПАКТНАЯ ВЕРСИЯ :: BY KAHS⚡",
            font=("Courier New", 10),
            text_color=NEON_THEME['text_dim']
        )
        footer.pack(side="bottom", pady=6)
    
    def _log(self, message: str):
        timestamp = time.strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}\n"
        if hasattr(self, 'log_text'):
            if hasattr(self, '_pending_logs') and self._pending_logs:
                for pending in self._pending_logs:
                    self.log_text.insert("end", pending + "\n")
                self._pending_logs.clear()
            self.log_text.insert("end", entry)
            self.log_text.see("end")
        else:
            if not hasattr(self, '_pending_logs'):
                self._pending_logs = []
            self._pending_logs.append(entry.rstrip())
    
    def _change_mode(self, value: str):
        mode_map = {
            "ЛАЙТ": Mode.LITE,
            "СТАНДАРТ": Mode.STANDARD,
            "АГРЕССИВ": Mode.AGGRESSIVE,
            "УЛЬТРА": Mode.ULTRA,
            "ПРОИЗВ.": Mode.PERFORMANCE,
            "УНИВЕРС.": Mode.UNIVERSAL,
            "ИГРОВОЙ": Mode.GAMING,
            "СТЕЛС": Mode.STEALTH,
            "ЭКСТРИМ": Mode.EXTREME,
            "РАНДОМ": Mode.RANDOM,
            "МУЛЬТИ": Mode.MULTI
        }
        
        mode = mode_map.get(value, Mode.UNIVERSAL)
        
        threading.Thread(
            target=lambda: self.process_manager.set_mode(mode),
            daemon=True
        ).start()
        
        self.config.set("mode", value)
        
        profile = DPIProfile.get_default_profiles()[mode]
        methods_str = ", ".join(profile.methods) if profile.methods else "базовый"
        self._log(f"[РЕЖИМ] {value} [{methods_str}]")
    
    def _start_dpi(self):
        self._update_status("active")
        self._log("▶ ЗАПУСК ПРОЦЕССА ОБХОДА DPI...")
        
        def start():
            success = self.process_manager.start()
            if success:
                profile = DPIProfile.get_default_profiles()[self.process_manager.current_mode]
                methods_count = len(profile.methods) if profile.methods else 1
                self._log(f"✅ DPI АКТИВИРОВАН (РЕЖИМ: {self.process_manager.current_mode.value})")
                self._log(f"📋 МЕТОДОВ: {methods_count}")
                if self.process_manager.packet_config.custom_methods:
                    self._log(f"📌 ПОЛЬЗОВАТЕЛЬСКИЙ МЕТОД: {self.process_manager.packet_config.custom_methods[:50]}...")
            else:
                self._log("❌ ОШИБКА ЗАПУСКА DPI")
                self._update_status("error")
        
        threading.Thread(target=start, daemon=True).start()
    
    def _stop_dpi(self):
        self._update_status("stopped")
        self._log("⏹ ОСТАНОВКА ПРОЦЕССА ОБХОДА DPI...")
        
        def stop():
            self.process_manager.stop()
            self._log("✅ DPI ДЕАКТИВИРОВАН")
        
        threading.Thread(target=stop, daemon=True).start()
    
    def _auto_start(self):
        self._log("▶ АВТОМАТИЧЕСКИЙ ЗАПУСК DPI...")
        self._start_dpi()
    
    def _update_status(self, status: str):
        if status == "active":
            self.status_indicator.configure(text_color=NEON_THEME['success'])
            self.status_label.configure(text="АКТИВЕН", text_color=NEON_THEME['success'])
        elif status == "stopped":
            self.status_indicator.configure(text_color=NEON_THEME['error'])
            self.status_label.configure(text="ОСТАНОВЛЕН", text_color=NEON_THEME['error'])
        elif status == "error":
            self.status_indicator.configure(text_color=NEON_THEME['warning'])
            self.status_label.configure(text="ОШИБКА", text_color=NEON_THEME['warning'])
    
    def _run_startup_checks(self):
        def run():
            self._log("─" * 50)
            self._log("▶ ЗАПУСК СТАРТОВЫХ ПРОВЕРОК...")
            
            running, info = self.service_manager.status_zapret()
            if running:
                self._log(f"[СТАТУС] ПРОЦЕСС ЗАПУЩЕН — {info}")
                self.after(0, lambda: self._update_status("active"))
                self.after(0, lambda: self.pid_label.configure(
                    text=info, text_color=NEON_THEME['success']))
            else:
                self._log("[СТАТУС] ПРОЦЕСС НЕ НАЙДЕН")
                self.after(0, lambda: self.pid_label.configure(
                    text="НЕТ ПРОЦЕССА", text_color=NEON_THEME['text_dim']))
            
            gf = self.service_manager.load_game_filter()
            if gf:
                self.process_manager.packet_config.game_filter = gf
                self._log(f"[GAME_FILTER] ЗАГРУЖЕНО: {gf[:60]}")
            
            self.after(0, lambda: self._log("─" * 50))
        
        threading.Thread(target=run, daemon=True).start()
        self.after(5000, self._periodic_status_check)
    
    def _periodic_status_check(self):
        def check():
            running, info = self.service_manager.status_zapret()
            if running:
                self.after(0, lambda: self._update_status("active"))
                self.after(0, lambda: self.pid_label.configure(
                    text=info, text_color=NEON_THEME['success']))
            else:
                if self.process_manager.is_running:
                    self.after(0, lambda: self._update_status("error"))
                    self.after(0, lambda: self.pid_label.configure(
                        text="ПРОЦЕСС УПАЛ", text_color=NEON_THEME['warning']))
                else:
                    self.after(0, lambda: self.pid_label.configure(
                        text="НЕТ ПРОЦЕССА", text_color=NEON_THEME['text_dim']))
        
        threading.Thread(target=check, daemon=True).start()
        self.after(5000, self._periodic_status_check)
    
    def _check_status_zapret_btn(self):
        self._log("▶ ПРОВЕРКА СТАТУСА ПРОЦЕССА...")
        self.btn_status_check.configure(state="disabled", text="⏳ ПРОВЕРКА...")
        
        def check():
            running, info = self.service_manager.status_zapret()
            if running:
                self._log(f"[СТАТУС] ЗАПУЩЕН — {info}")
                self.after(0, lambda: self._update_status("active"))
                self.after(0, lambda: self.pid_label.configure(
                    text=info, text_color=NEON_THEME['success']))
            else:
                self._log("[СТАТУС] ПРОЦЕСС НЕ НАЙДЕН")
                self.after(0, lambda: self._update_status("stopped"))
                self.after(0, lambda: self.pid_label.configure(
                    text="НЕТ ПРОЦЕССА", text_color=NEON_THEME['text_dim']))
            self.after(0, lambda: self.btn_status_check.configure(
                state="normal", text="🔍 СТАТУС"))
        
        threading.Thread(target=check, daemon=True).start()
    
    def _check_updates_btn(self):
        self._log("▶ ПРОВЕРКА ОБНОВЛЕНИЙ...")
        self.btn_updates.configure(state="disabled", text="⏳ ПРОВЕРКА...")
        
        def check():
            available, message = self.service_manager.check_updates()
            if available:
                self._log(f"[ОБНОВЛЕНИЯ] {message}")
            else:
                self._log(f"[ОБНОВЛЕНИЯ] {message}")
            self.after(0, lambda: self.btn_updates.configure(
                state="normal", text="📡 ОБНОВЛЕНИЯ"))
        
        threading.Thread(target=check, daemon=True).start()
    
    def _load_game_filter_btn(self):
        self._log("▶ ЗАГРУЗКА ИГРОВОГО ФИЛЬТРА...")
        
        def load():
            gf = self.service_manager.load_game_filter()
            if gf:
                self.process_manager.packet_config.game_filter = gf
                self._log(f"[GAME_FILTER] УСТАНОВЛЕН: {gf[:80]}")
                if self.process_manager.is_running:
                    self._log("▶ ПЕРЕЗАПУСК DPI С НОВЫМ ФИЛЬТРОМ...")
                    threading.Thread(
                        target=self.process_manager.restart, daemon=True).start()
            else:
                self._log("[GAME_FILTER] ФАЙЛ НЕ НАЙДЕН")
        
        threading.Thread(target=load, daemon=True).start()
    
    def _open_services(self):
        ServicesWindow(self, self.process_manager, self.config, self._log)
    
    def _open_autostart(self):
        AutostartWindow(self, self.config, self._log)
    
    def _open_help(self):
        HelpWindow(self)
    
    def _open_diagnostics(self):
        DiagnosticsWindow(self, self._log)
    
    def _open_packets(self):
        PacketWindow(self, self.process_manager, self.config, self._log)
    
    def _hide_window(self):
        self.withdraw()
    
    def _show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()
    
    def set_tray_icon(self, icon):
        self.tray_icon = icon


# ==============================================================================
# СИСТЕМНЫЙ ТРЕЙ С АНИМАЦИЕЙ
# ==============================================================================

class TrayManager:
    """Управление иконкой в системном трее с анимацией"""
    
    def __init__(self, app: MainApplication, process_manager: ProcessManager):
        self.app = app
        self.process_manager = process_manager
        self.icon = None
        self.animation_thread = None
        self.stop_animation = threading.Event()
        self.icon_created = threading.Event()
        self.icons = {}
        self.load_icons()
    
    def load_icons(self):
        """Загрузка иконок для трея"""
        config = ConfigManager()
        base_path = config.base_path
        
        def load_icon(filename, default_color):
            if getattr(sys, 'frozen', False):
                path = os.path.join(sys._MEIPASS, filename)
                if not os.path.exists(path):
                    path = os.path.join(base_path, filename)
            else:
                path = os.path.join(base_path, filename)
            
            try:
                if os.path.exists(path):
                    return Image.open(path)
            except Exception as e:
                print(f"Ошибка загрузки иконки {filename}: {e}")
            
            # Создаем иконку по умолчанию
            img = Image.new("RGB", (64, 64), default_color)
            draw = ImageDraw.Draw(img)
            draw.ellipse([16, 16, 48, 48], fill=default_color)
            draw.text((20, 24), "GZ", fill=(255, 255, 255))
            return img
        
        # Используем green.ico для всех состояний
        self.icons['blue'] = load_icon("blue.ico", (0, 150, 0))
        self.icons['green'] = load_icon("green.ico", (0, 150, 0))
        self.icons['red'] = load_icon("red.ico", (0, 150, 0))
    #   self.icons['yellow'] = load_icon("green.ico", (0, 150, 0))
    
    def create_icon(self):
        """Создание иконки в трее"""
        menu = pystray.Menu(
            item('⚡ ПОКАЗАТЬ ПАНЕЛЬ', lambda: self.show_window()),
            item('▶ ЗАПУСТИТЬ DPI', lambda: self.app._start_dpi()),
            item('⏹ ОСТАНОВИТЬ DPI', lambda: self.app._stop_dpi()),
            pystray.Menu.SEPARATOR,
            item('⚙ СЕРВИСЫ', lambda: self.app._open_services()),
            item('🔄 АВТОЗАПУСК', lambda: self.app._open_autostart()),
            item('📚 СПРАВКА', lambda: self.app._open_help()),
            pystray.Menu.SEPARATOR,
            item('❌ ВЫХОД', self.exit_app)
        )
        
        self.icon = pystray.Icon(
            "G-Zapret-Pro",
            self.icons.get('blue'),
            "GLOBAL-ZAPRET-PRO v5.2.0 ULTIMATE",
            menu
        )
        
        self.app.set_tray_icon(self.icon)
        self.icon_created.set()
        
        self.stop_animation.clear()
        self.animation_thread = threading.Thread(
            target=self.animate_icon,
            daemon=True
        )
        self.animation_thread.start()
        
        self.icon.run()
    
    def show_window(self):
        """Показать главное окно"""
        self.app._show_window()
    
    def animate_icon(self):
        """Анимация иконки в трее"""
        self.icon_created.wait()
        
        animation_sequence = ['blue', 'green', 'blue'] #'yellow']
        sequence_index = 0
        
        while not self.stop_animation.is_set():
            try:
                if self.process_manager.is_running:
                    # Активный режим - пульсирующая анимация (все иконки одинаковые)
                    self.icon.icon = self.icons.get(animation_sequence[sequence_index % len(animation_sequence)])
                    sequence_index += 1
                    time.sleep(0.5)
                else:
                    # Неактивный режим - статичная иконка
                    self.icon.icon = self.icons.get('red')
                    time.sleep(2.0)
                    
                    # Иногда мигаем для привлечения внимания
                    if not self.stop_animation.is_set():
                        self.icon.icon = self.icons.get('blue')
                        time.sleep(0.3)
            except Exception as e:
                print(f"Ошибка анимации: {e}")
                break
    
    def exit_app(self):
        """Выход из приложения"""
        self.stop_animation.set()
        self.process_manager.stop()
        
        if self.icon:
            self.icon.stop()
        
        self.app.quit()
        os._exit(0)


# ==============================================================================
# ТОЧКА ВХОДА
# ==============================================================================

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            " ".join(sys.argv) if not getattr(sys, 'frozen', False) else sys.argv[0],
            None,
            1
        )
        return
    
    ctk.set_appearance_mode(NEON_THEME['appearance'])
    ctk.set_default_color_theme("blue")
    
    app = MainApplication()
    
    tray = TrayManager(app, app.process_manager)
    tray_thread = threading.Thread(target=tray.create_icon, daemon=True)
    tray_thread.start()
    
    if ConfigManager().get("start_minimized", True):
        app.after(500, app._hide_window)
    
    app.mainloop()


if __name__ == "__main__":
    main()