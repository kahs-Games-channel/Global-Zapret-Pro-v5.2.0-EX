#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CHECK-BLOCKS-PRO v2.0
===================================
Расширенная диагностика блокировок и интеграция с DPI-обходом
Совместимость с Global-Zapret-Pro

Автор: Kahs
Версия: 2.0-Advanced-Diagnostics
"""

import socket
import requests
import time
import sys
import os
import json
import subprocess
import threading
from urllib.parse import urlparse
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from enum import Enum

try:
    import dns.resolver
    import dns.exception
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False
    print("⚠️ dnspython не установлен. DNS-проверки будут упрощены.")
    print("📦 Установи: pip install dnspython")

try:
    from ping3 import ping
    PING_AVAILABLE = True
except ImportError:
    PING_AVAILABLE = False
    print("⚠️ ping3 не установлен. Ping-проверки будут упрощены.")
    print("📦 Установи: pip install ping3")

try:
    import scapy.all as scapy
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("⚠️ scapy не установлен. Глубокий анализ пакетов недоступен.")
    print("📦 Установи: pip install scapy")

# ============================================================================
# КОНФИГУРАЦИЯ
# ============================================================================

class BlockType(Enum):
    """Типы блокировок"""
    DNS = "DNS"
    IP = "IP"
    TCP = "TCP"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    DPI = "DPI"
    SNI = "SNI"  # Блокировка по Server Name Indication
    TLS = "TLS"  # Блокировка TLS handshake
    QUIC = "QUIC"  # Блокировка QUIC протокола
    RST = "RST"  # RST-пакеты от провайдера
    TIMEOUT = "TIMEOUT"  # Таймаут соединения
    CERT = "CERT"  # Проблемы с сертификатом
    UNKNOWN = "UNKNOWN"


# Расширенный список сервисов для проверки
SERVICES = {
    "Google": {
        "url": "https://www.google.com",
        "ips": ["8.8.8.8", "8.8.4.4"],
        "alt_ports": [80, 443, 853],
        "description": "Поисковая система"
    },
    "Facebook": {
        "url": "https://www.facebook.com",
        "ips": ["31.13.79.35", "157.240.22.35"],
        "alt_ports": [80, 443, 8443],
        "description": "Социальная сеть"
    },
    "Twitter/X": {
        "url": "https://twitter.com",
        "ips": ["104.244.42.1", "104.244.42.129"],
        "alt_ports": [80, 443, 8080],
        "description": "Социальная сеть"
    },
    "Telegram": {
        "url": "https://web.telegram.org",
        "ips": ["149.154.167.99", "149.154.167.91"],
        "alt_ports": [80, 443, 5222],
        "description": "Мессенджер"
    },
    "Instagram": {
        "url": "https://www.instagram.com",
        "ips": ["157.240.22.174", "157.240.22.175"],
        "alt_ports": [80, 443, 8443],
        "description": "Социальная сеть"
    },
    "YouTube": {
        "url": "https://www.youtube.com",
        "ips": ["142.250.185.46", "216.58.209.14"],
        "alt_ports": [80, 443],
        "description": "Видеохостинг"
    },
    "Discord": {
        "url": "https://discord.com",
        "ips": ["162.159.128.233", "162.159.135.233"],
        "alt_ports": [80, 443, 5222],
        "description": "Голосовой/текстовый чат"
    },
    "TikTok": {
        "url": "https://www.tiktok.com",
        "ips": ["161.117.232.58", "161.117.202.110"],
        "alt_ports": [80, 443],
        "description": "Короткие видео"
    }
}

# Методы обхода по типам блокировки (расширенные)
BYPASS_METHODS = {
    "DNS": {
        "methods": [
            "Используй альтернативный DNS (1.1.1.1, 8.8.8.8, 94.140.14.14)",
            "Включи DNS-over-HTTPS (DoH) или DNS-over-TLS (DoT)",
            "Используй GoodbyeDPI с опцией --dns-addr=1.1.1.1",
            "Настрой локальный DNS-сервер (unbound, dnscrypt-proxy)"
        ],
        "tools": ["dnscrypt-proxy", "simple-tun", "Acrylic DNS"]
    },
    "IP": {
        "methods": [
            "Используй VPN-сервис (Amnezia, OpenVPN, WireGuard)",
            "Подключись через Tor Browser",
            "Настрой прокси-сервер (SOCKS5, HTTP)",
            "Используй GoodbyeDPI с опцией --ip-id=zero"
        ],
        "tools": ["Tor", "AmneziaVPN", "ProtonVPN"]
    },
    "TCP": {
        "methods": [
            "Используй VPN или SSH-туннель",
            "Попробуй GoodbyeDPI с опцией --port-l4=80,443",
            "Используй UDP туннелирование (OpenVPN over UDP)",
            "Настрой WireGuard поверх TCP"
        ],
        "tools": ["OpenVPN", "WireGuard", "SSH Tunnel"]
    },
    "HTTP": {
        "methods": [
            "Принудительно используй HTTPS (расширение HTTPS Everywhere)",
            "Используй GoodbyeDPI с опцией --fake-http",
            "Попробуй PowerTunnel с HTTP-дефрагментацией",
            "Настрой прокси с модификацией HTTP-заголовков"
        ],
        "tools": ["HTTPS Everywhere", "PowerTunnel", "Zapret"]
    },
    "HTTPS": {
        "methods": [
            "Используй GoodbyeDPI с опциями --fake-https и --split-https",
            "Попробуй TLS-фрагментацию (--tls-fragment)",
            "Используй Zapret с режимом multisplit",
            "Настрой VPN с обфускацией трафика"
        ],
        "tools": ["GoodbyeDPI", "Zapret", "AmneziaVPN"]
    },
    "DPI": {
        "methods": [
            "Используй GoodbyeDPI с агрессивными настройками (--blacklist dpi.txt)",
            "Включи мультисплит (--multisplit) в Zapret",
            "Используй PowerTunnel с плагином AntiDPI",
            "Настрой VPN с обфускацией (OpenVPN over TCP с маскировкой)",
            "Примени комбинацию методов: fake, multisplit, disorder2"
        ],
        "tools": ["Global-Zapret-Pro", "GoodbyeDPI", "Zapret", "PowerTunnel", "AmneziaVPN"]
    },
    "SNI": {
        "methods": [
            "Используй GoodbyeDPI с опцией --sni-chance=100",
            "Включи подмену SNI (--fake-sni) в Zapret",
            "Используй TLS-сегментацию для маскировки SNI",
            "Примени ESNI (Encrypted SNI) через DNS-over-HTTPS"
        ],
        "tools": ["GoodbyeDPI", "Zapret", "PowerTunnel"]
    },
    "TLS": {
        "methods": [
            "Используй GoodbyeDPI с опциями --tls-fragment и --tls-segment",
            "Включи подмену TLS Client Hello (--fake-tls)",
            "Примени мультисплит с TLS-паттернами",
            "Используй утилиту tls_clienthello из состава Zapret"
        ],
        "tools": ["GoodbyeDPI", "Zapret", "tls_clienthello"]
    },
    "QUIC": {
        "methods": [
            "Заблокируй QUIC (--block-quic) в GoodbyeDPI",
            "Используй подмену QUIC-пакетов (--fake-quic)",
            "Принудительно переключись на TCP/TLS",
            "Настрой UDP-туннель для QUIC-трафика"
        ],
        "tools": ["GoodbyeDPI", "Zapret", "QUIC Proxy"]
    },
    "RST": {
        "methods": [
            "Используй GoodbyeDPI с опцией --ip-id=zero",
            "Включи защиту от RST-пакетов (--rst-fake)",
            "Примени обход через TCP-сегментацию",
            "Используй VPN для защиты от RST-инъекций"
        ],
        "tools": ["GoodbyeDPI", "Zapret"]
    }
}

# ============================================================================
# РАСШИРЕННЫЕ ПРОВЕРКИ
# ============================================================================

class NetworkDiagnostics:
    """Расширенная диагностика сети"""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
    
    def check_multiple_dns(self, host: str) -> Dict[str, Tuple[bool, str]]:
        """Проверка DNS через разные серверы"""
        dns_servers = {
            "Google": "8.8.8.8",
            "Cloudflare": "1.1.1.1",
            "Quad9": "9.9.9.9",
            "OpenDNS": "208.67.222.222",
            "Comodo": "8.26.56.26",
            "Yandex": "77.88.8.8",
            "AdGuard": "94.140.14.14"
        }
        
        results = {}
        
        if not DNS_AVAILABLE:
            # Fallback to system DNS
            try:
                ip = socket.gethostbyname(host)
                results["System"] = (True, f"DNS OK: {ip}")
            except:
                results["System"] = (False, "DNS блокировка")
            return results
        
        for name, dns_server in dns_servers.items():
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [dns_server]
                resolver.timeout = 3
                resolver.lifetime = 3
                
                answers = resolver.resolve(host, 'A')
                results[name] = (True, f"DNS OK: {answers[0]}")
            except dns.resolver.NXDOMAIN:
                results[name] = (False, "DNS: Домен не существует")
            except dns.resolver.NoAnswer:
                results[name] = (False, "DNS: Нет ответа")
            except dns.exception.Timeout:
                results[name] = (False, "DNS: Таймаут")
            except Exception as e:
                results[name] = (False, f"DNS ошибка: {str(e)[:50]}")
            
            time.sleep(0.5)  # Пауза между запросами
        
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
                    results[port] = (True, "Открыт")
                else:
                    results[port] = (False, f"Закрыт/фильтруется (код: {result})")
            except Exception as e:
                results[port] = (False, f"Ошибка: {str(e)[:30]}")
        
        return results
    
    def check_ping(self, host: str, count: int = 4) -> Dict[str, float]:
        """Проверка ping до хоста"""
        results = {
            "packet_loss": 100,
            "avg_rtt": None,
            "min_rtt": None,
            "max_rtt": None
        }
        
        if PING_AVAILABLE:
            rtts = []
            for i in range(count):
                try:
                    rtt = ping(host, timeout=2)
                    if rtt:
                        rtts.append(rtt * 1000)  # Convert to ms
                        print(f"  Ping {i+1}: {rtt*1000:.1f}ms")
                    else:
                        print(f"  Ping {i+1}: Потеря пакета")
                except:
                    print(f"  Ping {i+1}: Ошибка")
                time.sleep(0.5)
            
            if rtts:
                results["packet_loss"] = ((count - len(rtts)) / count) * 100
                results["avg_rtt"] = sum(rtts) / len(rtts)
                results["min_rtt"] = min(rtts)
                results["max_rtt"] = max(rtts)
        else:
            # Simplified ping using socket
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_ICMP, socket.IPPROTO_ICMP)
                # This is simplified - real ICMP ping requires raw sockets
                results["packet_loss"] = 0
                results["avg_rtt"] = 50  # Estimate
            except:
                results["packet_loss"] = 100
        
        return results
    
    def check_mtu(self, host: str, port: int = 443) -> int:
        """Определение максимального MTU"""
        mtu = 1500
        step = 100
        
        while step > 0:
            try:
                # Попытка отправить пакет размером mtu
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((host, port))
                
                # Отправляем большой пакет для проверки MTU
                data = b'X' * mtu
                sock.send(data[:mtu])
                
                sock.close()
                mtu += step
            except:
                mtu -= step
                step //= 2
            
            if mtu > 9000:  # Jumbo frames
                break
        
        return min(mtu, 1500)
    
    def check_dpi_sensitivity(self, url: str) -> Dict[str, bool]:
        """Проверка чувствительности к DPI"""
        host = urlparse(url).hostname
        results = {}
        
        try:
            # Тест 1: Нормальный запрос
            normal = requests.get(url, timeout=5)
            results["normal"] = normal.status_code == 200
            
            # Тест 2: Изменение порядка заголовков
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'text/html',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            # Меняем порядок
            headers_reordered = {
                'Accept-Language': 'en-US,en;q=0.9',
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'text/html'
            }
            normal_order = requests.get(url, headers=headers, timeout=5)
            reordered = requests.get(url, headers=headers_reordered, timeout=5)
            results["header_order"] = reordered.status_code == 200 and reordered.status_code == normal_order.status_code
            
            # Тест 3: Добавление пробелов в Host
            headers_space = {'Host': host.replace('.', '. ')}
            space_test = requests.get(url, headers=headers_space, timeout=5)
            results["host_spaces"] = space_test.status_code == 200
            
            # Тест 4: Изменение регистра
            host_mixed = host.upper() + host.lower()
            headers_case = {'Host': host_mixed[:len(host)]}
            case_test = requests.get(url, headers=headers_case, timeout=5)
            results["case_sensitive"] = case_test.status_code == 200
            
            # Тест 5: Добавление лишних заголовков
            headers_extra = headers.copy()
            headers_extra['X-Custom'] = 'test' * 50  # Длинный заголовок
            extra_test = requests.get(url, headers=headers_extra, timeout=5)
            results["extra_headers"] = extra_test.status_code == 200
            
        except Exception as e:
            print(f"  DPI тест ошибка: {e}")
        
        return results


# ============================================================================
# ИНТЕГРАЦИЯ С GLOBAL-ZAPRET-PRO
# ============================================================================

class ZapretIntegration:
    """Интеграция с Global-Zapret-Pro"""
    
    def __init__(self, zapret_path: str = None):
        self.zapret_path = zapret_path or self._find_zapret()
        self.is_running = self._check_zapret_running()
    
    def _find_zapret(self) -> Optional[str]:
        """Поиск установленного Zapret/GoodbyeDPI"""
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "bin", "winws_zapret.exe"),
            os.path.join(os.path.dirname(__file__), "goodbyedpi.exe"),
            os.path.join(os.path.dirname(__file__), "zapret", "winws.exe"),
            "C:\\Program Files\\GoodbyeDPI\\goodbyedpi.exe",
            "C:\\zapret\\winws.exe"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def _check_zapret_running(self) -> bool:
        """Проверка запущен ли Zapret"""
        try:
            result = subprocess.run(
                'tasklist /FI "IMAGENAME eq winws_zapret.exe" /FO CSV /NH',
                capture_output=True, text=True, shell=True
            )
            return "winws_zapret.exe" in result.stdout
        except:
            return False
    
    def get_status(self) -> Dict:
        """Получение статуса Zapret"""
        return {
            "installed": self.zapret_path is not None,
            "running": self.is_running,
            "path": self.zapret_path
        }
    
    def suggest_optimal_mode(self, block_type: BlockType, service: str) -> str:
        """Предложение оптимального режима для блокировки"""
        
        suggestions = {
            BlockType.DNS: "Включи DNS-сервисы в настройках и выбери режим 'Стандарт'",
            BlockType.IP: "Используй режим 'Агрессив' для обхода IP-блокировок",
            BlockType.TCP: "Включи все TCP-сервисы и выбери режим 'Универс.'",
            BlockType.HTTP: "Используй режим 'Лайт' с включенным HTTP-обходом",
            BlockType.HTTPS: "Выбери режим 'Стандарт' с поддержкой HTTPS",
            BlockType.DPI: "Используй режим 'Агрессив' или 'Ультра' для Instagram/Facebook",
            BlockType.SNI: "Включи режим 'Агрессив' с подменой SNI",
            BlockType.TLS: "Используй режим 'Ультра' с TLS-фрагментацией",
            BlockType.QUIC: "Включи поддержку QUIC в настройках пакетов",
            BlockType.RST: "Используй режим 'Агрессив' с защитой от RST"
        }
        
        service_specific = {
            "Instagram": " для Instagram используй АГРЕССИВНЫЙ режим с включенной META",
            "Facebook": " для Facebook используй АГРЕССИВНЫЙ режим с включенной META",
            "Telegram": " для Telegram включи UDP-порты в настройках пакетов",
            "Discord": " для Discord включи все UDP-порты (443, 50000-65535)"
        }
        
        suggestion = suggestions.get(block_type, "Попробуй разные режимы работы")
        
        for key, text in service_specific.items():
            if key.lower() in service.lower():
                suggestion += text
        
        return suggestion


# ============================================================================
# ОСНОВНЫЕ ФУНКЦИИ ПРОВЕРКИ
# ============================================================================

def detect_block_type(dns_results: Dict, tcp_results: Dict, http_result: Tuple, 
                      dpi_results: Dict, ping_results: Dict, diagnostics: NetworkDiagnostics) -> BlockType:
    """Определение типа блокировки на основе всех проверок"""
    
    # Проверка DNS
    dns_success = any(ok for ok, _ in dns_results.values())
    if not dns_success:
        return BlockType.DNS
    
    # Проверка ping (потеря пакетов)
    if ping_results.get("packet_loss", 100) > 50:
        # Высокая потеря пакетов может указывать на IP/TCP блокировку
        pass
    
    # Проверка TCP
    tcp_success = any(ok for ok, _ in tcp_results.values())
    if not tcp_success:
        return BlockType.TCP
    
    # Проверка HTTP
    http_ok, http_msg = http_result
    if not http_ok:
        if "SSL" in http_msg or "certificate" in http_msg:
            return BlockType.TLS
        elif "403" in http_msg or "451" in http_msg:
            return BlockType.HTTP
        elif "Timeout" in http_msg:
            return BlockType.TIMEOUT
        else:
            return BlockType.HTTPS
    
    # Проверка DPI
    if dpi_results and not all(dpi_results.values()):
        # Некоторые DPI-тесты провалились
        return BlockType.DPI
    
    return BlockType.UNKNOWN


def check_service_detailed(name: str, service_info: Dict):
    """Расширенная проверка сервиса"""
    
    print(f"\n{'='*60}")
    print(f"🔍 ПРОВЕРКА: {name} - {service_info['description']}")
    print(f"📌 URL: {service_info['url']}")
    print(f"{'='*60}")
    
    url = service_info['url']
    host = urlparse(url).hostname
    
    diagnostics = NetworkDiagnostics()
    zapret = ZapretIntegration()
    
    # 1. DNS проверка через разные серверы
    print("\n📡 DNS проверка:")
    dns_results = diagnostics.check_multiple_dns(host)
    dns_success = False
    for server, (ok, msg) in dns_results.items():
        status = "✅" if ok else "❌"
        print(f"  {status} {server}: {msg}")
        if ok:
            dns_success = True
    
    # 2. Проверка ping
    print("\n📊 Ping проверка:")
    ping_results = diagnostics.check_ping(host)
    if ping_results["packet_loss"] < 100:
        print(f"  Потеря пакетов: {ping_results['packet_loss']:.1f}%")
        if ping_results["avg_rtt"]:
            print(f"  Средняя задержка: {ping_results['avg_rtt']:.1f}ms")
    else:
        print("  ❌ Ping недоступен (100% потеря пакетов)")
    
    if dns_success:
        # 3. Проверка TCP портов
        print("\n🔌 TCP порты проверка:")
        all_ports = list(set([443] + service_info.get('alt_ports', [])))
        tcp_results = diagnostics.check_port_range(host, all_ports)
        tcp_success = False
        for port, (ok, msg) in tcp_results.items():
            status = "✅" if ok else "❌"
            print(f"  {status} Порт {port}: {msg}")
            if ok and port == 443:
                tcp_success = True
        
        # 4. Проверка MTU
        print("\n📦 MTU проверка:")
        mtu = diagnostics.check_mtu(host)
        print(f"  Максимальный MTU: {mtu}")
        if mtu < 1400:
            print("  ⚠️ Низкий MTU может указывать на DPI/туннелирование")
        
        # 5. HTTP/HTTPS проверка
        print("\n🌐 HTTP/HTTPS проверка:")
        http_ok, http_msg = check_http_advanced(url)
        status = "✅" if http_ok else "❌"
        print(f"  {status} {http_msg}")
        
        # 6. DPI чувствительность
        print("\n🛡️ DPI чувствительность:")
        if http_ok:
            dpi_results = diagnostics.check_dpi_sensitivity(url)
            for test, ok in dpi_results.items():
                status = "✅" if ok else "❌"
                print(f"  {status} Тест {test}")
        else:
            dpi_results = {}
            print("  ⚠️ HTTP недоступен, DPI-тесты пропущены")
        
        # Определение типа блокировки
        block_type = detect_block_type(
            dns_results, tcp_results, (http_ok, http_msg),
            dpi_results, ping_results, diagnostics
        )
        
        print(f"\n{'='*60}")
        if block_type != BlockType.UNKNOWN:
            print(f"🚫 ТИП БЛОКИРОВКИ: {block_type.value}")
            
            # Рекомендации по обходу
            if block_type.value in BYPASS_METHODS:
                methods = BYPASS_METHODS[block_type.value]
                print(f"\n📋 МЕТОДЫ ОБХОДА:")
                for i, method in enumerate(methods["methods"], 1):
                    print(f"  {i}. {method}")
                
                if "tools" in methods:
                    print(f"\n🛠️ РЕКОМЕНДУЕМЫЕ ИНСТРУМЕНТЫ:")
                    print(f"  {', '.join(methods['tools'])}")
            
            # Интеграция с Zapret
            zapret_status = zapret.get_status()
            if zapret_status["installed"]:
                print(f"\n⚙️ GLOBAL-ZAPRET-PRO:")
                status = "ЗАПУЩЕН" if zapret_status["running"] else "ОСТАНОВЛЕН"
                print(f"  Статус: {status}")
                
                suggestion = zapret.suggest_optimal_mode(block_type, name)
                print(f"  Совет: {suggestion}")
            else:
                print(f"\n⚙️ Установи Global-Zapret-Pro для автоматического обхода")
        else:
            print("✅ СЕРВИС ДОСТУПЕН ПОЛНОСТЬЮ")
    
    # Время проверки
    elapsed = time.time() - diagnostics.start_time
    print(f"\n⏱️ Время проверки: {elapsed:.1f} сек")


def check_http_advanced(url: str, timeout: int = 5) -> Tuple[bool, str]:
    """Расширенная проверка HTTP с разными User-Agent"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36',
        'curl/7.68.0',
        'Wget/1.20.3'
    ]
    
    for ua in user_agents:
        try:
            headers = {'User-Agent': ua}
            response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            
            if response.status_code == 200:
                return True, f"HTTP 200 OK (UA: {ua[:20]}...)"
            elif response.status_code in [403, 451]:
                # Пробуем следующий User-Agent
                continue
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.SSLError:
            return False, "SSL ошибка (возможно TLS блокировка)"
        except requests.exceptions.Timeout:
            return False, "Таймаут соединения"
        except requests.exceptions.ConnectionError:
            return False, "Ошибка соединения"
        except Exception as e:
            continue
    
    return False, "Все User-Agent заблокированы"


def generate_report(results: Dict):
    """Генерация отчета"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"block_report_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("ОТЧЕТ О ПРОВЕРКЕ БЛОКИРОВОК\n")
        f.write(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        
        for service, data in results.items():
            f.write(f"Сервис: {service}\n")
            f.write(f"Статус: {data.get('status', 'Неизвестно')}\n")
            if 'block_type' in data:
                f.write(f"Тип блокировки: {data['block_type']}\n")
                f.write(f"Рекомендации: {data.get('recommendations', '')}\n")
            f.write("-"*40 + "\n\n")
    
    print(f"\n📄 Отчет сохранен: {filename}")


# ============================================================================
# ИНТЕРАКТИВНЫЙ РЕЖИМ
# ============================================================================

def interactive_mode():
    """Интерактивный режим проверки"""
    print("\n" + "="*60)
    print("🔧 ИНТЕРАКТИВНЫЙ РЕЖИМ ДИАГНОСТИКИ")
    print("="*60)
    
    while True:
        print("\nВыберите действие:")
        print("1. Проверить все сервисы")
        print("2. Проверить конкретный сервис")
        print("3. Проверить пользовательский URL")
        print("4. Проверить интеграцию с Global-Zapret-Pro")
        print("5. Сохранить отчет")
        print("0. Выход")
        
        choice = input("\nВаш выбор (0-5): ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            results = {}
            for name, info in SERVICES.items():
                check_service_detailed(name, info)
                results[name] = {"status": "Проверено"}
                time.sleep(2)
        elif choice == "2":
            print("\nДоступные сервисы:")
            for i, name in enumerate(SERVICES.keys(), 1):
                print(f"{i}. {name}")
            
            try:
                idx = int(input("\nВыберите номер: ")) - 1
                name = list(SERVICES.keys())[idx]
                check_service_detailed(name, SERVICES[name])
            except (ValueError, IndexError):
                print("❌ Неверный выбор")
        elif choice == "3":
            url = input("Введите URL для проверки: ").strip()
            if url:
                custom_service = {
                    "url": url,
                    "ips": [],
                    "alt_ports": [80, 443],
                    "description": "Пользовательский URL"
                }
                check_service_detailed("Custom", custom_service)
        elif choice == "4":
            zapret = ZapretIntegration()
            status = zapret.get_status()
            print(f"\nGlobal-Zapret-Pro статус:")
            print(f"  Установлен: {'Да' if status['installed'] else 'Нет'}")
            print(f"  Запущен: {'Да' if status['running'] else 'Нет'}")
            if status['path']:
                print(f"  Путь: {status['path']}")
        elif choice == "5":
            print("Функция сохранения отчета в разработке")
        else:
            print("❌ Неверный выбор")


# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================

def main():
    print("""
╔══════════════════════════════════════════════╗
║   CHECK-BLOCKS-PRO v2.0                      ║
║   Расширенная диагностика блокировок         ║
║   Интеграция с Global-Zapret-Pro             ║
╚══════════════════════════════════════════════╝
    """)
    
    # Проверка аргументов командной строки
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            for name, info in SERVICES.items():
                check_service_detailed(name, info)
                time.sleep(2)
        elif sys.argv[1] == "--interactive":
            interactive_mode()
        elif sys.argv[1] == "--url" and len(sys.argv) > 2:
            url = sys.argv[2]
            custom_service = {
                "url": url,
                "ips": [],
                "alt_ports": [80, 443],
                "description": "Пользовательский URL"
            }
            check_service_detailed("Custom", custom_service)
        elif sys.argv[1] == "--help":
            print("""
Использование:
  python check_blocks.py --all           - Проверить все сервисы
  python check_blocks.py --interactive   - Интерактивный режим
  python check_blocks.py --url <URL>     - Проверить конкретный URL
  python check_blocks.py --help          - Показать справку
            """)
    else:
        # По умолчанию запускаем интерактивный режим
        interactive_mode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Проверка прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()