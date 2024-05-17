# Import necessary packages
from sqlalchemy import Table, Column, Integer, Float, String, Boolean, Enum, create_engine, MetaData, inspect, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from geoalchemy2 import Geometry
from mysql import connector


# Define function to create data model


def create_data_model(db_name, db_user, db_password, db_host, db_port):
    """Creates a data model for storing telecommunication infrastructure information.

    This function creates a data model for a database containing information about
    telecommunication infrastructure elements like Points of Interest (POIs), cell sites,
    transmission nodes, and analyses performed on this infrastructure.

    Warning: This function will drop all tables and data in the database if they already exist, before creating new tables.

    The data model consists of the following tables:
    - Analysis: Contains information about analyses performed on the infrastructure.
    - PointOfInterest: Contains information about Points of Interest (POIs) in the infrastructure.
    - CellSite: Contains information about cell sites in the infrastructure.
    - TransmissionNode: Contains information about transmission nodes in the infrastructure.
    - CellCoverage: Contains information about mobile coverage contours in the infrastructure.
    - CostParameter: Contains cost parameters for the cost model.
    - MappingResult: Contains mapping results for POIs.
    - VisibilityResult: Contains visibility results for POIs.
    - FiberPathResultPOI: Contains fiber path results for POIs.
    - FiberPathResultEdge: Contains fiber path results for edges.
    - FiberPathResultNode: Contains fiber path results for nodes.
    - CostResultPOI: Contains cost results for POIs.
    - CostResult: Contains cost results for technology assignment solutions.

    Args:
        use_local (bool, optional): Flag to indicate using a local development database.
            Defaults to True.

    Returns:
        None
    """

    # Connect to existing database and drop tables
    try:
        # Connect to existing database
        with connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
        ) as existing_database:

            # Create cursor object
            with existing_database.cursor() as cursor:

                # Set foreign key checks to 0
                command = "SET FOREIGN_KEY_CHECKS=0"
                cursor.execute(command)
                existing_database.commit()

                # List of tables to drop
                tables_to_drop = ["analysis", "cell_site", "cost_parameter", "point_of_interest", "transmission_node", "cell_coverage",
                                  "mapping_result", "visibility_result", "fiber_path_result_poi", "fiber_path_result_edge", "fiber_path_result_node",
                                  "cost_result", "cost_result_poi",
                                  "analysis_cellsite_association", "analysis_poi_association", "analysis_transmissionnode_association", "analysis_coverage_association"]

                for table in tables_to_drop:
                    # Drop table (if exists) for each table in the list
                    command = f"DROP TABLE IF EXISTS {table}"
                    cursor.execute(command)
                    existing_database.commit()

                # Set foreign key checks back to 1
                command = "SET FOREIGN_KEY_CHECKS=1"
                cursor.execute(command)
                existing_database.commit()

    except connector.Error as e:
        print(e)

    # Connect to database using SQLAlchemy
    db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url, echo=False)

    # Define base class for all database models and reflect tables
    Base = declarative_base()
    Base.metadata.reflect(bind=engine)
    table_names = Base.metadata.tables.keys()

    # Check if there are any tables in the database
    if len(table_names) == 0:
        print("All tables have been deleted from the database.")
    else:
        # Print table names
        print("Tables already in the database:")
        for table_name in table_names:
            print(table_name)

    # Define association tables for many-to-many relationships
    # POIs used in each analysis
    analysis_poi_association = Table('analysis_poi_association', Base.metadata,
                                     Column(
                                         'analysis_id', String(50), ForeignKey('analysis.analysis_id')),
                                     Column(
                                         'poi_id', String(50), ForeignKey('point_of_interest.poi_id'))
                                     )

    # Cell sites used in each analysis
    analysis_cellsite_association = Table('analysis_cellsite_association', Base.metadata,
                                          Column(
                                              'analysis_id', String(50), ForeignKey('analysis.analysis_id')),
                                          Column(
                                              'ict_id', String(50), ForeignKey('cell_site.ict_id'))
                                          )

    # Transmission nodes used in each analysis
    analysis_transmissionnode_association = Table('analysis_transmissionnode_association', Base.metadata,
                                                  Column(
                                                      'analysis_id', String(50), ForeignKey('analysis.analysis_id')),
                                                  Column(
                                                      'node_id', String(50), ForeignKey('transmission_node.node_id'))
                                                  )

    # Mobile coverage contours used in each analysis
    analysis_coverage_association = Table('analysis_coverage_association', Base.metadata,
                                          Column(
                                              'analysis_id', String(50), ForeignKey('analysis.analysis_id')),
                                          Column(
                                              'contour_id', Integer, ForeignKey('cell_coverage.contour_id'))
                                          )

    # Define Analysis table
    class Analysis(Base):
        # Table name
        __tablename__ = 'analysis'

        # Columns
        analysis_id = Column(String(50), primary_key=True)
        cost_parameter_id = Column(String(50), ForeignKey('cost_parameter.cost_id'))

        # Define relationships with Costs, POIs, Cell Sites and Transmission Nodes
        cost_parameter = relationship("CostParameter", back_populates="analyses")
        pointsofinterest = relationship(
            "PointOfInterest",
            secondary=analysis_poi_association,
            back_populates="analyses")
        cellsites = relationship(
            "CellSite",
            secondary=analysis_cellsite_association,
            back_populates="analyses")
        transmissionnodes = relationship(
            "TransmissionNode",
            secondary=analysis_transmissionnode_association,
            back_populates="analyses")
        coveragecontours = relationship(
            "CellCoverage",
            secondary=analysis_coverage_association,
            back_populates="analyses")

    # Define Point of interest table
    class PointOfInterest(Base):
        # Table name
        __tablename__ = 'point_of_interest'

        # Define Enum for ConnectivityType
        ConnectivityType = Enum(
            "unknown", "mobile", "mobile_broadband", "metro", "fiber", "wireless", "satellite", "wired",
            name="connectivity_type_enum"
        )

        # Columns
        poi_id = Column(String(50), primary_key=True)
        source_poi_id = Column(String(50))
        dataset_id = Column(String(50), nullable=False, index=True)
        lat = Column(Float, nullable=False, index=True)
        lon = Column(Float, nullable=False, index=True)
        connectivity_type = Column(ConnectivityType, index=True)  # Using Enum for connectivity type
        poi_type = Column(String(50), nullable=False)
        is_public = Column(Boolean)
        poi_subtype = Column(String(50))
        country_code = Column(String(3), nullable=False)
        admin1 = Column(String(100))
        admin2 = Column(String(100))
        admin3 = Column(String(100))
        is_connected = Column(Boolean, index=True)
        has_electricity = Column(Boolean)
        electricity_type = Column(String(50))
        label = Column(String(50))

        # Define the relationships with other tables
        analyses = relationship(
            "Analysis",
            secondary=analysis_poi_association,
            back_populates="pointsofinterest")
        mapping_result = relationship("MappingResult", back_populates="point_of_interest")
        visibility_result = relationship("VisibilityResult", back_populates="point_of_interest")
        fiber_path_result_poi = relationship(
            "FiberPathResultPOI", back_populates="point_of_interest")
        cost_result_poi = relationship("CostResultPOI", back_populates="point_of_interest")

    # Define Cell site table
    class CellSite(Base):
        # Table name
        __tablename__ = 'cell_site'

        # Define Enum for radio type
        RadioType = Enum(
            "2G", "3G", "4G", "5G",
            name="radio_type_enum"
        )

        # Define Enum for backhaul type
        BackhaulType = Enum(
            "fiber", "microwave", "satellite",
            name="backhaul_type_enum"
        )

        # Define Enum for power source
        PowerSource = Enum(
            "grid", "generator", "solar",
            name="power_source_enum"
        )

        # Columns
        ict_id = Column(String(50), primary_key=True)
        source_ict_id = Column(String(50), index=True)
        source_cell_id = Column(String(50))
        dataset_id = Column(String(50), nullable=False, index=True)
        country_code = Column(String(3), nullable=False)
        lat = Column(Float, nullable=False, index=True)
        lon = Column(Float, nullable=False, index=True)
        admin1 = Column(String(100))
        admin2 = Column(String(100))
        admin3 = Column(String(100))
        operator_name = Column(String(100))
        radio_type = Column(RadioType, index=True)
        downlink_frequency_mhz = Column(Float)
        uplink_frequency_mhz = Column(Float)
        max_channel_bandwidth_mhz = Column(Float)
        eirp_dbm = Column(Float)
        tower_height = Column(Float)
        antenna_height = Column(Float)
        mechanical_tilt_degrees = Column(Float)
        electrical_tilt_degrees = Column(Float)
        azimuth_degrees = Column(Float)
        antenna_model = Column(String(100))
        antenna_gain = Column(Float)
        antenna_horizontal_beamwidth_degrees = Column(Float)
        antenna_vertical_beamwidth_degrees = Column(Float)
        backhaul_type = Column(BackhaulType, index=True)
        backhaul_throuput_mbps = Column(Float)
        power_source = Column(PowerSource, index=True)

        # Define the relationships with other tables
        analyses = relationship(
            "Analysis",
            secondary=analysis_cellsite_association,
            back_populates="cellsites")

    # Define Transmission node table
    class TransmissionNode(Base):
        # Table name
        __tablename__ = 'transmission_node'

        # Enum for transmission medium
        TransmissionMedium = Enum(
            "fiber", "microwave", "copper", "coaxial", "unknown",
            name="transmission_medium_enum"
        )

        # Enum for backhaul technologies
        BackhaulTechnologies = Enum(
            "dwdm", "sdh", "tdm", "sonet",
            name="backhaul_technologies_enum"
        )

        # Enum for node status
        NodeStatus = Enum(
            "proposed", "planned", "underconstruction", "operational", "decommissioned", "inactive",
            name="node_status_enum"
        )

        # Enum for power source
        PowerSource = Enum(
            "grid", "generator", "solar",
            name="power_source_enum"
        )

        # Columns
        node_id = Column(String(50), primary_key=True)
        source_ict_id = Column(String(50))
        dataset_id = Column(String(50), nullable=False, index=True)
        country_code = Column(String(3), nullable=False, index=True)
        lat = Column(Float, nullable=False, index=True)
        lon = Column(Float, nullable=False, index=True)
        admin1 = Column(String(100))
        admin2 = Column(String(100))
        admin3 = Column(String(100))
        physical_infrastructure_provider = Column(String(100))
        network_providers = Column(String(100))
        transmission_medium = Column(TransmissionMedium, index=True)
        access_technologies = Column(String(100))
        backhaul_technologies = Column(BackhaulTechnologies, index=True)
        is_actual = Column(Boolean, nullable=False)
        node_status = Column(NodeStatus, index=True)
        equipped_capacity_access_mbps = Column(Integer)
        potential_capacity_access_mbps = Column(Integer)
        equipped_capacity_backhaul_mbps = Column(Integer)
        potential_capacity_backhaul_mbps = Column(Integer)
        is_powered = Column(Boolean)
        power_source = Column(PowerSource, index=True)

        # Define the relationships with other tables
        analyses = relationship(
            "Analysis",
            secondary=analysis_transmissionnode_association,
            back_populates="transmissionnodes")

    # Define Cell coverage table
    class CellCoverage(Base):
        # Table name
        __tablename__ = 'cell_coverage'

        # Columns
        contour_id = Column(Integer, primary_key=True)
        fid = Column(Integer)
        ID = Column(Integer)
        layer = Column(Integer)
        path = Column(String(50))
        coverage = Column(Integer, nullable=False)

        # Define the relationships with other tables
        analyses = relationship(
            "Analysis",
            secondary=analysis_transmissionnode_association,
            back_populates="coveragecontours")

    # Define Cost parameter table

    class CostParameter(Base):
        # Table name
        __tablename__ = 'cost_parameter'

        # Columns
        cost_id = Column(String(50), primary_key=True)
        hw_setup_cost_fiber = Column(Float, nullable=False)
        focl_constr_cost_fiber = Column(Float, nullable=False)
        reinv_period_fiber = Column(Float, nullable=False)
        an_hw_maint_and_repl_fiber = Column(Float, nullable=False)
        pp_fiber = Column(Float, nullable=False)
        an_traffic_fees_one_mbps_fiber = Column(Float, nullable=False)
        an_isp_fees_one_mbps_fiber = Column(Float, nullable=False)
        ch_throughput_fiber = Column(Float, nullable=False)
        hw_setup_cost_p2mp = Column(Float, nullable=False)
        reinv_period_p2mp = Column(Float, nullable=False)
        an_hw_maint_and_repl_p2mp = Column(Float, nullable=False)
        pp_p2mp = Column(Float, nullable=False)
        an_traffic_fees_one_mbps_p2mp = Column(Float, nullable=False)
        an_isp_fees_one_mbps_p2mp = Column(Float, nullable=False)
        ch_throughput_p2mp = Column(Float, nullable=False)
        hw_setup_cost_p2p = Column(Float, nullable=False)
        access_link_setup_p2p = Column(Float, nullable=False)
        backhaul_link_num_p2p = Column(Float, nullable=False)
        backhaul_link_setup_p2p = Column(Float, nullable=False)
        retr_tower_num_p2p = Column(Float, nullable=False)
        retr_tower_inst_p2p = Column(Float, nullable=False)
        access_link_bandwidth_p2p = Column(Float, nullable=False)
        backhaul_link_bandwidth_p2p = Column(Float, nullable=False)
        one_time_license_fee_1mhz_p2p = Column(Float, nullable=False)
        an_license_fee_1mhz_p2p = Column(Float, nullable=False)
        an_traffic_fees_one_mbps_p2p = Column(Float, nullable=False)
        an_isp_fees_one_mbps_p2p = Column(Float, nullable=False)
        ch_throughput_p2p = Column(Float, nullable=False)
        hw_setup_cost_sat = Column(Float, nullable=False)
        reinv_period_sat = Column(Float, nullable=False)
        an_hw_maint_and_repl_sat = Column(Float, nullable=False)
        pp_sat = Column(Float, nullable=False)
        an_traffic_fees_one_mbps_sat = Column(Float, nullable=False)
        an_isp_fees_one_mbps_sat = Column(Float, nullable=False)
        ch_throughput_sat = Column(Float, nullable=False)

        # Define the relationships with other tables
        analyses = relationship("Analysis", back_populates="cost_parameter")

    # Define Mapping results table

    class MappingResult(Base):
        # Table name
        __tablename__ = 'mapping_result'

        # Columns
        id = Column(String(50), primary_key=True)
        poi_id = Column(
            String(50),
            ForeignKey('point_of_interest.poi_id'),
            nullable=False)
        lat = Column(Float, nullable=False)
        lon = Column(Float, nullable=False)
        cell_site_dist = Column(Float)
        _4G_cell_site_dist = Column(Float)
        _5G_cell_site_dist = Column(Float)
        transmission_node_dist = Column(Float)
        fiber_node_dist = Column(Float)
        population_1km = Column(Integer)
        poi_count_1km = Column(Integer)
        population_3km = Column(Integer)
        poi_count_3km = Column(Integer)
        population_5km = Column(Integer)
        poi_count_5km = Column(Integer)
        _4G_coverage = Column(Boolean)

        # Define the relationships with other tables
        point_of_interest = relationship(
            "PointOfInterest", back_populates="mapping_result")

    # Define Visibility results table

    class VisibilityResult(Base):
        # Table name
        __tablename__ = 'visibility_result'

        # Columns
        id = Column(String(50), primary_key=True)
        poi_id = Column(
            String(50),
            ForeignKey('point_of_interest.poi_id'),
            nullable=False)

        # Visibility results
        is_visible = Column(Boolean)
        num_visible = Column(Integer)

        # First cell site
        cellsite_1 = Column(String(50))
        lat_1 = Column(Float)
        lon_1 = Column(Float)
        radio_type_1 = Column(String(50))
        ground_distance_1 = Column(Float)
        antenna_los_distance_1 = Column(Float)
        azimuth_angle_1 = Column(Float)
        los_geometry_1 = Column(String(50))

        # Second cell site
        cellsite_2 = Column(String(50))
        lat_2 = Column(Float)
        lon_2 = Column(Float)
        radio_type_2 = Column(String(50))
        ground_distance_2 = Column(Float)
        antenna_los_distance_2 = Column(Float)
        azimuth_angle_2 = Column(Float)
        los_geometry_2 = Column(String(50))

        # Third cell site
        cellsite_3 = Column(String(50))
        lat_3 = Column(Float)
        lon_3 = Column(Float)
        radio_type_3 = Column(String(50))
        ground_distance_3 = Column(Float)
        antenna_los_distance_3 = Column(Float)
        azimuth_angle_3 = Column(Float)
        los_geometry_3 = Column(String(50))

        # Define the relationships with other tables
        point_of_interest = relationship(
            "PointOfInterest", back_populates="visibility_result")

    # Define Fiber path results tables - POI level

    class FiberPathResultPOI(Base):
        # Table name
        __tablename__ = 'fiber_path_result_poi'

        # Columns
        id = Column(String(50), primary_key=True)
        poi_id = Column(
            String(50),
            ForeignKey('point_of_interest.poi_id'),
            nullable=False)
        closest_node_id = Column(String(50))
        closest_node_distance = Column(Float)
        connected_node_id = Column(String(50))
        connected_node_distance = Column(Float)
        fiber_path = Column(String(50))
        upstream_node_id = Column(String(50))
        upstream_node_distance = Column(Float)

        # Define the relationships with other tables
        point_of_interest = relationship(
            "PointOfInterest",
            back_populates="fiber_path_result_poi")

    # Define Fiber path results tables - edge level

    class FiberPathResultEdge(Base):
        # Table name
        __tablename__ = 'fiber_path_result_edge'

        # Columns
        edge_id = Column(Integer, primary_key=True)
        u = Column(Integer)
        v = Column(Integer)
        key = Column(Integer)
        length = Column(Integer)
        geometry = Column(Geometry('LINESTRING'))
        name = Column(String(50))
        osmid = Column(Integer)
        highway = Column(String(50))
        oneway = Column(Integer)
        reversed = Column(Integer)
        lanes = Column(Integer)
        service = Column(String(50))
        ref = Column(String(50))
        maxspeed = Column(Integer)
        bridge = Column(String(50))
        junction = Column(String(50))
        access = Column(String(50))

    # Define Fiber path results tables - node level

    class FiberPathResultNode(Base):
        # Table name
        __tablename__ = 'fiber_path_result_node'

        # Columns
        node_id = Column(Integer, primary_key=True)
        osmid = Column(String(50))
        y = Column(Float)
        x = Column(Float)
        splitter = Column(String(50))
        street_count = Column(Integer)
        lon = Column(Float)
        lat = Column(Float)
        geometry = Column(Geometry('POINT'))
        highway = Column(String(50))

    # Define Cost results tables - POI level

    class CostResultPOI(Base):
        # Table name
        __tablename__ = 'cost_result_poi'

        # Columns
        id = Column(String(50), primary_key=True)
        poi_id = Column(
            String(50),
            ForeignKey('point_of_interest.poi_id'),
            nullable=False)
        lat = Column(Float)
        lon = Column(Float)
        cell_site_dist = Column(Float)
        _4G_coverage = Column(Integer)
        is_connected = Column(Integer)
        is_visible = Column(Boolean)
        num_visible = Column(Integer)

        # Define fiber length and MST solution columns for each kilometer
        for i in range(1, 26):
            locals()[f'fiber_length_{i}km'] = Column(Float)
            locals()[f'mst_solution_{i}km'] = Column(Integer)
            locals()[f'technology_{i}km'] = Column(String(50))

        # Define the relationships with other tables
        point_of_interest = relationship(
            "PointOfInterest", back_populates="cost_result_poi")

    # Define Cost results tables - technology assignment solution level

    class CostResult(Base):
        # Table name
        __tablename__ = 'cost_result'

        # Columns
        id = Column(String(50), primary_key=True)
        technology_selection_approach = Column(String(50))
        basket_name = Column(String(50))
        technology = Column(String(50))
        number_poi = Column(Integer)
        fiber_length = Column(Float)
        pp_coo = Column(Float)
        pp_coo_per_poi = Column(Float)
        pp_capex = Column(Float)
        init_capex = Column(Float)
        an_opex = Column(Float)
        init_capex_per_poi = Column(Float)
        an_opex_per_poi = Column(Float)
        p2p = Column(String(50))
        estimate = Column(Float)
        max_dist_km = Column(Integer)

    # Create all tables defined in Base
    Base.metadata.create_all(engine)

    # Commit changes
    Session = sessionmaker(bind=engine)
    session = Session()
    session.commit()

    # Check created tables

    try:
        # Connect to existing database
        with connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        ) as existing_database:

            # Create cursor object
            with existing_database.cursor() as cursor:

                # Show tables
                command = "SHOW TABLES"
                cursor.execute(command)

                # Fetch and print table names (assuming table name is the first element)
                print("The following tables were added:")
                for table in cursor:
                    print(table[0])

    except connector.Error as e:
        print(e)

    print("Database model created and committed.")