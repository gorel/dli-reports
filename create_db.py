import os

from dli_app import db

from dli_app.mod_auth.models import (
    Department,
    Location,
    RegisterCandidate,
    User,
)

from dli_app.mod_reports.models import (
    Field,
    FieldData,
    FieldType,
    Report,
    Tag,
)

from dli_app.mod_wiki.models import (
    WikiPage,
)

WIKIPAGE_HOME_CONTENT = """
# DLI Policies Wiki
Welcome to DLI's Policies Wiki!
"""


def populate_db_departments():
    """Populate the database Department model"""
    departments = [
        Department('Account Development'),
        Department('Composition'),
        Department('Customer Service'),
        Department('Electronic Art'),
        Department('Order Processing'),
        Department('Plates'),
        Department('Press'),
        Department('Process Color'),
        Department('Shipping'),
    ]
    db.session.add_all(departments)


def populate_db_locations():
    """Populate the database Location model"""
    locations = [
        Location('New Albany'),
        Location('Omaha'),
    ]
    db.session.add_all(locations)


def populate_db_users():
    """Populate the database User model"""
    users = [
        User(
            name='Nobody',
            email='nobody@dli.report',
            password=os.environ['DLI_REPORTS_ADMIN_PASSWORD'],
            location=Location.query.first(),
            department=Department.query.first(),
        ),
    ]
    db.session.add_all(users)


def populate_db_fieldtypes():
    """Populate the database FieldType model"""
    types = [
        FieldType('currency'),
        FieldType('double'),
        FieldType('integer'),
        FieldType('string'),
        FieldType('time'),
    ]
    db.session.add_all(types)


def populate_db_fields():
    """Populate the database Field model

    Populate the database Field model by adding all fields that DLI currently
    uses on its 8:40 morning report. This will allow us to quickly have a
    populated and complete database whenever we have to drop all tables.
    """

    from dli_app.mod_reports.models import FieldTypeConstants
    FieldTypeConstants.reload()

    ad = Department.query.filter_by(name='Account Development').first()
    comp = Department.query.filter_by(name='Composition').first()
    cs = Department.query.filter_by(name='Customer Service').first()
    ea = Department.query.filter_by(name='Electronic Art').first()
    op = Department.query.filter_by(name='Order Processing').first()
    plates = Department.query.filter_by(name='Plates').first()
    press = Department.query.filter_by(name='Press').first()
    pc = Department.query.filter_by(name='Process Color').first()
    shipping = Department.query.filter_by(name='Shipping').first()

    fields = [
        # Department: Account Development
        Field(
            name='Orders Entered',
            ftype=FieldTypeConstants.INTEGER,
            department=ad,
        ),
        Field(
            name='Sales Entered',
            ftype=FieldTypeConstants.CURRENCY,
            department=ad,
        ),
        Field(
            name='Orders Pending',
            ftype=FieldTypeConstants.INTEGER,
            department=ad,
        ),
        Field(
            name='Sales Pending',
            ftype=FieldTypeConstants.CURRENCY,
            department=ad,
        ),
        Field(
            name='Total In House Sales',
            ftype=FieldTypeConstants.CURRENCY,
            department=ad,
        ),
        Field(
            name='New Albany Sales',
            ftype=FieldTypeConstants.CURRENCY,
            department=ad,
        ),
        Field(
            name='Omaha Sales',
            ftype=FieldTypeConstants.CURRENCY,
            department=ad,
        ),
        Field(
            name='Quotes Given',
            ftype=FieldTypeConstants.INTEGER,
            department=ad,
        ),
        Field(
            name='Quotes Pending',
            ftype=FieldTypeConstants.INTEGER,
            department=ad,
        ),

        # Department: Composition
        Field(
            name='Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=comp,
        ),
        Field(
            name='Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=comp,
        ),
        Field(
            name='In Department',
            ftype=FieldTypeConstants.INTEGER,
            department=comp,
        ),

        # Department: Customer Service
        Field(
            name='In House',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='Due',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='CMYK',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='Redos',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='DLI On Time Percentage',
            ftype=FieldTypeConstants.DOUBLE,
            department=cs,
        ),
        Field(
            name='CMYK On Time Percentage',
            ftype=FieldTypeConstants.DOUBLE,
            department=cs,
        ),
        Field(
            name='Omaha On Time Percentage',
            ftype=FieldTypeConstants.DOUBLE,
            department=cs,
        ),
        Field(
            name='Total On Time Percentage',
            ftype=FieldTypeConstants.DOUBLE,
            department=cs,
        ),
        Field(
            name='Omaha Redos',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='Total Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='2-Day Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='3-Day Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='CMYK Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='Omaha Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='CS Number of Calls',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='CS Number Answered',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='CS Percentage Within Service',
            ftype=FieldTypeConstants.DOUBLE,
            department=cs,
        ),
        Field(
            name='CS Average Delay',
            ftype=FieldTypeConstants.TIME,
            department=cs,
        ),
        Field(
            name='Status Number of Calls',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='Status Number Answered',
            ftype=FieldTypeConstants.INTEGER,
            department=cs,
        ),
        Field(
            name='Status Percentage Within Service',
            ftype=FieldTypeConstants.DOUBLE,
            department=cs,
        ),
        Field(
            name='Status Average Delay',
            ftype=FieldTypeConstants.TIME,
            department=cs,
        ),

        # Department: Electronic Art
        Field(
            name='Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=ea,
        ),
        Field(
            name='Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=ea,
        ),
        Field(
            name='In Department',
            ftype=FieldTypeConstants.INTEGER,
            department=ea,
        ),

        # Department: Order Processing
        Field(
            name='Adjusted Sales',
            ftype=FieldTypeConstants.CURRENCY,
            department=op,
        ),
        Field(
            name='Backlog',
            ftype=FieldTypeConstants.CURRENCY,
            department=op,
        ),
        Field(
            name='Total Labels Entered',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Manual Entered',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='EW Entered',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Total Stamps Entered',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Total Entered',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='EW Pending',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='EW OE Average',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Percentage in EW',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='EW Reorders',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Manual to Composition',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Manual to Shipping',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Manual to Press',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Total Manual',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Total DLI EW',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Total Omaha EW',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Total into Production',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Quotes Received (#)',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Quotes Received ($)',
            ftype=FieldTypeConstants.CURRENCY,
            department=op,
        ),
        Field(
            name='Screenprint Received (#)',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Screenprint Received ($)',
            ftype=FieldTypeConstants.CURRENCY,
            department=op,
        ),
        Field(
            name='Magnets Received (#)',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Magnets Received ($)',
            ftype=FieldTypeConstants.CURRENCY,
            department=op,
        ),
        Field(
            name='Online Quotes',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Total Quotes',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Online Quotes Percentage',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Web Order Status',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='LabelNet Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='LabelNet Sales',
            ftype=FieldTypeConstants.CURRENCY,
            department=op,
        ),
        Field(
            name='Manual Left Over',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='EW Left Over',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Quotes Left Over',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Omaha Left Over',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='OP Catelog Requests Given',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='OP Catelog Requests Pending',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='CQ Requests Given',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='CQ Requests Pending',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='OP QA Pending',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Quote QA Pending',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='CMYK QA Pending',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='OP Number of Calls',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='OP Number Answered',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='OP Percentage Within Service',
            ftype=FieldTypeConstants.DOUBLE,
            department=op,
        ),
        Field(
            name='OP Average Delay',
            ftype=FieldTypeConstants.TIME,
            department=op,
        ),
        Field(
            name='CQ Number of Calls',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='CQ Number Answered',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='CQ Percentage Within Service',
            ftype=FieldTypeConstants.DOUBLE,
            department=op,
        ),
        Field(
            name='CQ Average Delay',
            ftype=FieldTypeConstants.TIME,
            department=op,
        ),
        Field(
            name='DLI EW Projection',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Omaha EW Projection',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Manual Projection',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Saturday Projection',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),
        Field(
            name='Total Projection',
            ftype=FieldTypeConstants.INTEGER,
            department=op,
        ),

        # Department: Plates
        Field(
            name='To Press Due (New Albany)',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='To Press Late (New Albany)',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='To Press Total (New Albany)',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='To Press Due (Omaha)',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='To Press Late (Omaha)',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='To Press Total (Omaha)',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='To Press Due (Process)',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='To Press Late (Process)',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='To Press Total (Process)',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='Total Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='Total Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='Saturday Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='Saturday Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='In Department Due',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='In Department Late',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='In Department Total',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='Press Returns',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),
        Field(
            name='Prepress Returns',
            ftype=FieldTypeConstants.INTEGER,
            department=plates,
        ),

        # Department: Press
        Field(
            name='Day Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Day Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Night Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Night Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='3rd Shift Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='3rd Shift Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Saturday Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Saturday Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Total Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Total Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Average Imp',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Average Tri',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Average Process',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Average Laser',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Average 650',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Average 650C',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Average 450',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Average HP',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Average HP Total',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Total Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Imp Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Tri Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='450 Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='650 Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Digital Spot Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Ditial CMYK Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Flexo CMYK Lates',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='In Department',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='To Print',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Projected',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Days',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Nights',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='3rd Shift',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Saturdays',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: Imp',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: Imp Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: C#',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: C# Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: FF/EMB',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: FF/EMB Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: 650',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: 650 Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: 650C',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: 650C Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: 450',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: 450 Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: REW',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: REW Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: P Laser',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: P Laser Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: BLASER',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: BLASER Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: Process',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: Process Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: TRI/UB',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: TRI/UB Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: HP',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: HP Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: ABG',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: ABG Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: OCE',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: OCE Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: Jet',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: Jet Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: RDC',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: RDC Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),
        Field(
            name='Orders on Press: LDC',
            ftype=FieldTypeConstants.INTEGER,
            department=press,
        ),
        Field(
            name='Orders on Press: LDC Status',
            ftype=FieldTypeConstants.STRING,
            department=press,
        ),

        # Department: Process Color
        Field(
            name='Digital in Production',
            ftype=FieldTypeConstants.INTEGER,
            department=pc,
        ),
        Field(
            name='Digital In Department',
            ftype=FieldTypeConstants.INTEGER,
            department=pc,
        ),
        Field(
            name='Flexo in Production',
            ftype=FieldTypeConstants.INTEGER,
            department=pc,
        ),
        Field(
            name='Flexo In Department',
            ftype=FieldTypeConstants.INTEGER,
            department=pc,
        ),

        # Department: Shipping
        Field(
            name='Day Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Day Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Night Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Night Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Total Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Total Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Saturday Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Saturday Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Week Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Week Copies',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Shipped Early',
            ftype=FieldTypeConstants.CURRENCY,
            department=shipping,
        ),
        Field(
            name='In Department',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Late Orders',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Orders Packed',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='SWOG Holding',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='New Albany Rejects',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Omaha Rejects',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Projected',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Days',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Nights',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Saturday',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Number of Trucks',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Number of Boxes',
            ftype=FieldTypeConstants.INTEGER,
            department=shipping,
        ),
        Field(
            name='Total Truck Sales',
            ftype=FieldTypeConstants.CURRENCY,
            department=shipping,
        ),
    ]
    db.session.add_all(fields)


def populate_db_tags():
    """Populate the database Tag model"""
    tags = [
        Tag('all'),
        Tag('dli'),
        Tag('morning'),
    ]
    db.session.add_all(tags)


def populate_db_reports():
    """Populate the database Report model"""
    reports = [
        Report(
            user_id=User.query.first().id,
            name='8:40 Report',
            fields=Field.query.all(),
            tags=Tag.query.all(),
        ),
    ]
    db.session.add_all(reports)


def populate_db_wikipages():
    """Populate the database WikiPage model"""
    pages = [
        WikiPage(
            name='home',
            content=WIKIPAGE_HOME_CONTENT,
        ),
    ]
    db.session.add_all(pages)


def populate_db_all():
    """Completely populate a basic db for DLI"""
    if 'DLI_REPORTS_ADMIN_PASSWORD' not in os.environ:
        print('Please set env variable DLI_REPORTS_ADMIN_PASSWORD first.')
        return

    populate_db_departments()
    db.session.commit()
    populate_db_locations()
    db.session.commit()
    populate_db_users()
    db.session.commit()
    populate_db_fieldtypes()
    db.session.commit()
    populate_db_fields()
    db.session.commit()
    populate_db_tags()
    db.session.commit()
    populate_db_reports()
    db.session.commit()
    populate_db_wikipages()
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
