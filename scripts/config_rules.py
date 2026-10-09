# scripts/config_rules.py
import os

GITHUB_REPO_ENV = os.environ.get('GITHUB_REPOSITORY', '')
if '/' in GITHUB_REPO_ENV:
    GITHUB_USER, REPO_NAME = GITHUB_REPO_ENV.split('/', 1)
else:
    GITHUB_USER, REPO_NAME = 'nexgen999', 'PS5-Super-PLDMGR-Auto-Updater-Core_OS'  
BASE_URL = f"https://{GITHUB_USER}.github.io/{REPO_NAME}"

PATHS = {
    "feed_dir": "feed",
    "json_dir": "json",
    "payloads_dir": "payloads",
    "rss_dir": "rss",
    "archives_dir": "archives",
    "categories": {
        "payloads": {"feed": "feed/payloads", "json": "json/payloads", "root": "payloads"},
        "pkg": {"feed": "feed/pkg", "json": "json/pkg"},
        "ffpfsc": {"feed": "feed/ffpfsc", "json": "json/ffpfsc"},
        "apps": {"feed": "feed/apps", "json": "json/apps"},
    }
}

# =========================================================================
# MOTEUR DE RÈGLES UNIFIÉ ET GRANULAIRE PAR DÉPÔT
# =========================================================================
REPO_RULES = {
    # Option globale pour activer la détection automatique des pré-releases en cas d'absence de release stable
    "global_settings": {
        "auto_fallback_pre_release": True
    },
    "custom_payload_rules": {
        
        # --- Dépôt saawant12/orbit-store-ps5 (Bloquer le gros zip source bundle) ---
        "saawant12/orbit-store-ps5": {
            "release_channel": "stable",
            "allowed_extensions": [".elf"],
            "exclude_keywords": ["source-bundle", "source"],
            "download_source_archive": False,
            "keep_original": True,
            "strict_clean": True,
            "targets": [
                {
                    "match": "orbit_store",
                    "rename": "orbit_store_v{version}.elf"
                }
            ]
        },

        # --- 1. Dépôts avec conservation du nom d'origine ---
        "smoxa/ps5-new-overlay": {
            "keep_original": True,
            "strict_clean": True,
            "release_channel": "stable",
            "allowed_extensions": [".elf"],
            "exclude_extensions": [],
            "exclude_keywords": [],
            "extract_zip": False,
            "download_source_archive": False,
            "targets": []
        },
        "instalador-host-psm-poop2jb": {
            "extract_zip": True,
            "keep_original": True,
            "release_channel": "stable",
            "strict_clean": False
        },
        "psm": {
            "keep_original": True,
            "release_channel": "stable"
        },
        "poords4": {
            "extract_zip": True,
            "keep_original": True,
            "release_channel": "stable"
        },

        # --- 2. Dépôts avec extraction de ZIP ou fichiers ELF récents ---
        "drakmor/shadowmountplus": {
            "extract_zip": False,
            "release_channel": "pre-release",
            "allowed_extensions": [".elf"],
            "keep_original": True,
            "strict_clean": False
        },
        "shadowmountplus": {
            "extract_zip": False,
            "release_channel": "pre-release",
            "allowed_extensions": [".elf"],
            "keep_original": True,
            "strict_clean": False
        },
        "fan_target": {
            "extract_zip": True,
            "suffix_format": "_{temperature}_v{version}.elf",
            "release_channel": "stable"
        },
        "drakmor/fan_target": {
            "extract_zip": True,
            "suffix_format": "_{temperature}_v{version}.elf",
            "release_channel": "stable",
            "allowed_extensions": [".zip", ".elf"]
        },

        # --- 3. Dépôts avec nettoyage strict ---
        "ps5-payload-dev/websrv": {
            "strict_clean": True,
            "release_channel": "stable"
        },
        "phantomptr/ps5upload": {
            "strict_clean": True,
            "release_channel": "stable"
        },
        "boazvdwansem/ps5-debugger": {
            "strict_clean": True,
            "release_channel": "stable"
        },

        # --- 4. Dépôts configurés (Stables & Pre-Releases) ---
        "blackbearreloaded/ProsperoEden": {
            "release_channel": "pre-release",
            "allowed_extensions": [".ffpfsc"],
            "strict_clean": True,
        },
        "rdiol12/ps5library": {
            "release_channel": "pre-release",
            "allowed_extensions": [".elf"],
            "strict_clean": True,
            "targets": [
                {
                    "match": "ps5library-agent",
                    "rename": "ps5library-agent_v{version}.elf"
                }
            ]
        },
        "itsblurf/bfplayer": {
            "release_channel": "pre-release",
            "allowed_extensions": [".elf"],
            "strict_clean": True,
            "targets": [
                {
                    "match": "bfplayer-standalone",
                    "rename": "bfplayer-standalone_v{version}.elf"
                }
            ]
        },
        "illusionyy/ps5-fw-spoof": {
            "release_channel": "pre-release",
            "allowed_extensions": [".elf"],
            "strict_clean": True,
            "targets": [
                {
                    "match": "ps5-fw-spoof",
                    "rename": "ps5-fw-spoof_v{version}.elf"
                }
            ]
        },
        "notmaj0r/prosperomgr": {
            "release_channel": "stable",
            "allowed_extensions": [".elf"],
            "strict_clean": True,
            "targets": [
                {
                    "match": "ProsperoMgr",
                    "rename": "ProsperoMgr_v{version}.elf"
                }
            ]
        },
        
        # --- Nouveaux Dépôts (ZIP en Pre-Release) ---
        "tsuramatsu1/Vita3K-PS5": {
            "release_channel": "pre-release",
            "allowed_extensions": [".zip"],
            "keep_original": True,
            "strict_clean": True,
            "extract_zip": False,
            "targets": []
        },
        "romanocry/EmuStore-PS5": {
            "release_channel": "pre-release",
            "allowed_extensions": [".zip"],
            "keep_original": True,
            "strict_clean": True,
            "extract_zip": False,
            "targets": []
        },
        
        # --- Dépôts idlesauce (Multi-ELF) ---
        "idlesauce/ps5-self-decrypter": {
            "release_channel": "stable",
            "allowed_extensions": [".elf"],
            "keep_original": True,
            "strict_clean": True,
            "targets": [
                {"match": "ps5-self-decrypter-full-system", "rename": "ps5-self-decrypter-full-system_v{version}.elf"},
                {"match": "ps5-self-decrypter-game", "rename": "ps5-self-decrypter-game_v{version}.elf"},
                {"match": "ps5-self-decrypter-shellcore", "rename": "ps5-self-decrypter-shellcore_v{version}.elf"},
                {"match": "ps5-self-decrypter-system-common-lib", "rename": "ps5-self-decrypter-system-common-lib_v{version}.elf"}
            ]
        },
        "idlesauce/ps5-self-pager": {
            "release_channel": "stable",
            "allowed_extensions": [".elf"],
            "keep_original": True,
            "strict_clean": True,
            "targets": [
                {"match": "ps5-self-pager-full-system", "rename": "ps5-self-pager-full-system_v{version}.elf"},
                {"match": "ps5-self-pager-game", "rename": "ps5-self-pager-game_v{version}.elf"},
                {"match": "ps5-self-pager-shellcore", "rename": "ps5-self-pager-shellcore_v{version}.elf"},
                {"match": "ps5-self-pager-system-common-lib", "rename": "ps5-self-pager-system-common-lib_v{version}.elf"}
            ]
        },

        # --- Dépôt Forgejo earthonion/np-fake-signin (Version PS5 uniquement) ---
        "earthonion/np-fake-signin": {
            "release_channel": "stable",
            "allowed_extensions": [".elf"],
            "exclude_keywords": ["ps4"],
            "keep_original": True,
            "strict_clean": True,
            "targets": [
                {
                    "match": "np-fake-signin-ps5",
                    "rename": "np-fake-signin_v{version}.elf"
                }
            ]
        },

        # --- Dépôt SvenGDK/Prospero-Multi-Tools (Apps ZIP) ---
        "SvenGDK/Prospero-Multi-Tools": {
            "release_channel": "stable",
            "allowed_extensions": [".zip"],
            "keep_original": True,
            "strict_clean": True,
            "targets": [
                {
                    "match": "EmulatorPack",
                    "rename": "ProsperoMultiTools_EmulatorPack.zip"
                }
            ]
        },

        # --- Dépôt StonedModder/ActRemoteLink-13.x (Multi-ELF) ---
        "StonedModder/ActRemoteLink-13.x": {
            "release_channel": "stable",
            "allowed_extensions": [".elf"],
            "keep_original": True,
            "strict_clean": True,
            "targets": [
                {"match": "actremotelink_agent", "rename": "actremotelink_agent_v{version}.elf"},
                {"match": "actremotelink_pin_notify", "rename": "actremotelink_pin_notify_v{version}.elf"}
            ]
        },

        # --- 5. Dépôts avec mappings spécifiques et règles poussées ---
        "seregonwar/zftpd": {
            "release_channel": "stable",
            "allowed_extensions": [".elf"],
            "exclude_extensions": [".bin"],
            "exclude_keywords": ["-ps4-"],
            "keep_original": False,
            "strict_clean": True,
            "extract_zip": False,
            "download_source_archive": False,
            "mapping": {
                "zftpd-ps5-v1.6.0.elf": "zftpd_v{version}.elf",
                "zftpd-ps5-zhttp-v1.6.0.elf": "zhttp_v{version}.elf"
            },
            "targets": [
                {
                    "match": "zftpd-ps5-v1.6.0.elf",
                    "rename": "zftpd_v{version}.elf"
                },
                {
                    "match": "zftpd-ps5-zhttp-v1.6.0.elf",
                    "rename": "zhttp_v{version}.elf"
                }
            ]
        },
        "owendswang/ps5-web-file-manager": {
            "release_channel": "stable",
            "keep_original": True,
            "strict_clean": False,
            "mapping": {
                "web-file-mgr": "web-file-mgr_v{version}.elf",
                "wfm-7zip-helper.elf": "wfm-7zip-helper.elf"
            },
            "targets": []
        }
    }
}

# Configuration par défaut appliquée si un dépôt n'est pas explicitement déclaré ci-dessus
DEFAULT_REPO_CONFIG = {
    "release_channel": "stable",
    "allowed_extensions": [".elf", ".bin", ".ffpfsc", ".zip"],
    "exclude_extensions": [".txt", ".exe", ".dmg"],
    "exclude_keywords": [],
    "keep_original": False,
    "strict_clean": False,
    "extract_zip": False,
    "download_source_archive": False,
    "mapping": {},
    "targets": []
}

DISALLOWED_EXTENSIONS = ('.dmg', '.exe', '.appimage', '.msi', '.txt')
