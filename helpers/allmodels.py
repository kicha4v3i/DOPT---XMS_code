from custom_auth.models import User,Rights,Companies,Modules,Enquiry,Userlog,Countries,Poamainmodules,CountryUsers
from projects.models import Projects,ProjectUsers,ProjectBlock,ProjectField
from wells.models import Wells,WellUsers,CoordinateSystems,Projections
from pressure.models import Pressure
from mud.models import MudPumpFlowRate,MudPumpData,MudPump
from django.db.models import Count, Min, Sum, Avg , Max
from pressureloss.models import Calculationchartdata
from mud.models import MudPump,PumpManufacturer,Pumps
from muddata.models import MudData,Rheogram,RheogramNameModels,RheogramDate,Sections,MudType,RheogramSections
from drillbitdata.models import DrillBit,DrillBitNozzle,BitTypesNames
from bhadata.models import BhaData,BhaElement,Drillcollers,Drillpipe,DrillpipeHWDP,Specifications,Pressuredroptool,Empirical,Differential_pressure
from wellphases.models import WellPhases
from ticket.models import Tickets,Ticketattachments,Ticketrecipient





