from pydantic import BaseModel

# Terminal Properties
class TerminalProperty(BaseModel):
    # Boolean Properties
    community_account: bool  # Presence of MQL5.community authorization data
    community_connection: bool  # Connection to MQL5.community
    connected: bool  # Connection to a trade server
    dlls_allowed: bool  # Permission to use DLL
    trade_allowed: bool  # Permission to trade
    tradeapi_disabled: bool  # Trade API disabled flag
    email_enabled: bool  # Permission to send e-mails
    ftp_enabled: bool  # Permission to send reports using FTP
    notifications_enabled: bool  # Permission to send notifications to smartphone
    mqid: bool  # Presence of MetaQuotes ID for Push notifications

    # Integer Properties
    build: int  # The client terminal build number
    maxbars: int  # The maximal bars count on the chart
    codepage: int  # Code page number of the language
    ping_last: int  # Last known ping to trade server (microseconds)

    # Float Properties
    community_balance: float  # Balance in MQL5.community
    retransmission: float  # Percentage of resent network packets

    # String Properties
    company: str  # Company name
    name: str  # Terminal name
    language: str  # Language of the terminal
    path: str  # Folder from which the terminal is started
    data_path: str  # Folder where terminal data are stored
    commondata_path: str  # Common path for all terminals
