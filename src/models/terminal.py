from pydantic import BaseModel
from enum import IntEnum


# Terminal Enumerations
class TerminalColorTheme(IntEnum):
    """Terminal color theme enumeration"""
    LIGHT = 0
    DARK = 1


class ThemeColor(IntEnum):
    """Theme color constants for UI elements"""
    WINDOW = 0  # Window background
    WINDOWTEXT = 1  # Text in the window
    BTNTEXT = 2  # Button text
    GRAYTEXT = 3  # Inactive (disabled) text
    INFOTEXT = 4  # Tooltip text
    INFOBK = 5  # Tooltip background
    FACE_3D = 6  # Front face of 3D elements
    LIGHT_3D = 7  # Light side of 3D elements
    SHADOW_3D = 8  # Shadow side of 3D elements
    DKSHADOW_3D = 9  # Dark shadow of 3D elements
    HILIGHT_3D = 10  # Highlight of 3D elements
    HIGHLIGHT = 11  # Background of selected elements
    HIGHLIGHTTEXT = 12  # Text of selected elements
    BTNFACE = 13  # Button front face
    BTNHILIGHT = 14  # Button highlight
    BTNSHADOW = 15  # Button shadow
    MENU = 16  # Menu background
    MENUBAR = 17  # Menu bar background
    MENUTEXT = 18  # Menu text
    MENUHILIGHT = 19  # Highlight of selected menu item
    ACTIVECAPTION = 20  # Active window title
    INACTIVECAPTION = 21  # Inactive window title
    GRADIENTINACTIVECAPTION = 22  # Gradient of inactive window title
    CAPTIONTEXT = 23  # Window title text
    INACTIVECAPTIONTEXT = 24  # Inactive window title text
    HOTTEXT = 25  # Hyperlinks or active elements
    NONE = 26  # Color not selected
    SEPARATOR = 27  # Separator
    SCROLLBACK = 28  # Scrollbar
    LINE1 = 29  # Background color of odd rows in the Journal
    LINE2 = 30  # Background color of even rows in the Journal
    GRID = 31  # Grid color in the Journal
    SUMMARY = 32  # Background color of summary row in the Journal
    ERROR = 33  # Error message text color
    INVALID = 34  # Invalid value text color
    NEGATIVE = 35  # Negative value color
    POSITIVE = 36  # Positive value color
    LINK = 37  # Link color
    LINKHOVER = 38  # Link hover color
    LINKTESTER = 39  # Link color from cached results
    TEXTUP = 40  # "Button released" state
    TEXTDOWN = 41  # "Button pressed" state
    BACKUP = 42  # Color of "BUY"/"SELL" buttons when quote increases
    BACKDOWN = 43  # Color of "BUY"/"SELL" buttons when quote decreases
    CLOSE = 44  # "Close" operation button color
    BUY = 45  # "BUY" operation button color
    SELL = 46  # "SELL" operation button color
    DEPOSIT = 47  # "Deposit" button color
    WITHDRAWAL = 48  # "Withdrawal" button color
    BID = 49  # Bid line color
    ASK = 50  # Ask line color
    STOPS = 51  # Stop line color
    STOPS_RED = 52  # StopLoss highlight when profit is negative
    STOPS_GREEN = 53  # StopLoss highlight when profit is positive
    CONFIRM = 54  # "Accept" button color in order window
    REQUOTE = 55  # "Requote" button color in order window
    REJECT = 56  # "Reject" button color in order window
    NOTIFICATION = 57  # Change notification color
    RATING = 58  # Rating bar color
    BOOK_BUY = 59  # Background color of buy levels in Depth of Market
    BOOK_SELL = 60  # Background color of sell levels in Depth of Market
    BOOK_LAST = 61  # Color of last trade in Depth of Market
    BOOK_STOP = 62  # StopLoss level color in Depth of Market
    BOOK_SPREAD = 63  # Background color of spread levels
    TICKS_BID = 64  # Bid line color on tick chart
    TICKS_ASK = 65  # Ask line color on tick chart
    TICKS_LAST = 66  # Last line color on tick chart
    TICKS_CROSS = 67  # Crosshair color on tick chart
    TICKS_SL = 68  # StopLoss line color on tick chart
    TICKS_TP = 69  # TakeProfit line color on tick chart
    TESTER_START = 70  # "Start" button color in testing
    TESTER_STOP = 71  # "Stop" button color in testing
    TESTER_START_FRAME = 72  # Border color of "Start" button
    TESTER_STOP_FRAME = 73  # Border color of "Stop" button
    TESTER_PROGRESS = 74  # Progress bar color
    TESTER_BALANCE = 75  # Balance line color in Strategy Tester
    TESTER_EQUITY = 76  # Equity line color in Strategy Tester
    TESTER_MARGIN = 77  # Deposit Load graph color
    PROFILER_CALL = 78  # Color of code line with call
    PROFILER_CALLSEL = 79  # Selected code line color with call
    PROFILER_LINE = 80  # Line color in Profiler Journal
    PROFILER_LINESEL = 81  # Selected line color in Profiler Journal


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
