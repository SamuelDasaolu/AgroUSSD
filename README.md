### **A 4-day Team Project Challenge on Nigerian Agricultural USSD System**
**Project Overview**

- Your team will build AgroUSSD, a simple USSD-based agricultural information system that helps Nigerian farmers access real-time market prices and manage basic crop information. This system simulates USSD interactions through a console interface, making it accessible to farmers with basic mobile phones.

**Problem Statement**
 - Meet Adamu


 Adamu is a 45-year-old tomato farmer from Kano State who cultivates 3 hectares of farmland. Every harvest season tells the same heartbreaking story. Monday morning at 6:00 AM, Adamu wakes up to check his tomato crop - 500 crates ready for harvest after months of hard work, investment in seeds, fertilizers, and sleepless nights protecting his farm. Tuesday at 8:00 AM, he contacts Mallam Sani, the local middleman who has been buying from farmers for 15 years. Sani offers ₦800 per crate. Adamu has no idea that tomatoes are selling for ₦2,200 per crate in Lagos markets and ₦1,800 in Abuja. Wednesday, Adamu reluctantly accepts Sani's offer of ₦400,000 for his entire harvest, not knowing that restaurants in nearby Kaduna are desperately seeking fresh tomatoes and willing to pay ₦1,500 per crate - almost double Sani's price. Thursday, Sani transports the tomatoes to Lagos and sells them for ₦1,100,000, making ₦700,000 profit while Adamu struggles to recover his farming costs of ₦350,000, leaving him with just ₦50,000 profit for months of labor.

- Meet Kemi

Kemi owns three restaurants in Abuja and faces her own challenges. Every morning, she drives 45 minutes to Mile 12 market, fighting traffic and paying high transportation costs to buy vegetables at inflated prices from multiple middlemen. She never knows daily prices until she arrives at the market, making it impossible to plan her restaurant menus and pricing effectively. By the time produce reaches her through 3-4 middlemen, vegetables are often wilted, reducing her restaurant's food quality. During rainy seasons or transport strikes, she sometimes can't get vegetables at all, forcing her to close her restaurants or serve limited menus. Kemi often thinks: "If only I could buy directly from farmers like Adamu, we would both benefit - I'd get fresher produce at better prices, and farmers would earn more for their hard work."

This story repeats across Nigeria's 70 million smallholder farmers

- 40% of harvest is lost to post-harvest waste due to poor market connections
- Middlemen capture 60-70% of final selling prices
- Farmers remain trapped in poverty despite feeding the nation
- Buyers pay premium prices for lower quality produce
- The economy loses billions in agricultural value due to inefficient markets


- Nigerian agricultural commerce is trapped in a cycle of inefficiency that impoverishes farmers and inflates costs for consumers. The core challenges include:
1. Information Asymmetry Crisis

Farmers lack real-time market price information across different locations
No visibility into demand patterns or seasonal price trends
Limited knowledge of alternative buyers and market opportunities

2. Middleman Exploitation System

Farmers forced to accept below-market prices due to lack of alternatives
Multiple layers of middlemen inflate final prices by 200-400%
No direct connection channels between farmers and end buyers

3. Market Access Barriers

Rural farmers cannot reach urban markets due to transportation costs
No platform for farmers to advertise their products and prices
Buyers cannot locate specific farmers or products in their regions

4. Technology Gap

Most agricultural solutions require smartphones and internet access
85% of rural farmers only have basic mobile phones with USSD capability
Existing platforms are too complex for farmers with limited digital literacy

5. Economic Impact

Farmers earn 20-30% of final retail prices for their products
Post-harvest losses reach 40% due to poor market connections
Agricultural productivity growth stagnates despite increasing food demand

**What you are Required to do**

- To democratize agricultural commerce in Nigeria by creating an accessible, USSD-based digital marketplace that connects farmers directly with buyers, eliminates exploitative middlemen, and empowers farmers with market information and fair pricing opportunities.
- Transform Nigeria's agricultural value chain by leveraging basic mobile technology to create direct farmer-buyer relationships, ensuring farmers receive fair prices while buyers access fresh, affordable produce.

**Core Objectives**

1. Empower Farmers:

- Provide real-time market price information across multiple locations
- Enable farmers to set their own competitive prices
- Create direct channels to reach buyers without middlemen
- Build farmer profiles showcasing their products and contact information

2. Enable Buyers:

- Connect directly with farmers in specific locations
- Access transparent pricing and product availability information
- Reduce procurement costs by eliminating middleman markups
- Ensure fresh produce supply through direct farmer relationships

3. Transform the Market:

- Create price transparency across the agricultural value chain
- Reduce post-harvest waste through better market connections
- Increase farmers' income by 150-300% through direct sales
- Build a sustainable, technology-enabled agricultural ecosystem

**Requirements**

- Functional Requirements
1. User Management System

 - Farmer Registration: Name, phone, location, farm size, primary crops
 - User Authentication: PIN-based login system
 - Profile Management: Update contact information and farming details

2. Market Information System

  - Price Checking: Real-time prices by product and location
  - Market Comparison: Compare prices across different markets
  - Historical Trends: Basic price movement information

3. Harvest Management & Marketplace

  - Harvest Recording: Log harvest quantity, quality, and asking price
  - Product Listing: Create marketplace entries with pricing
  - Inventory Tracking: Monitor available products and quantities

4. Buyer Connection Platform

  - Farmer Directory: Search farmers by location and products
  - Contact Sharing: Provide farmer phone numbers to interested buyers
  - Direct Communication: Facilitate buyer-farmer connections

5. USSD Interface Simulation

  - Menu Navigation: Intuitive, hierarchical menu system
  - Session Management: Maintain user state across interactions

**Technical Requirements**

- Core Technologies & Constraints

  - Programming Language: Python 3.8+
  - Interface: Command Line Interface (CLI) simulating USSD interactions
  - Architecture: Object-Oriented Programming with strict focus on:

   - Class Inheritance: Base classes with specialized implementations
  - Abstraction: Abstract base classes defining system contracts


- Data Storage: File-based persistence (JSON/CSV) - no databases
 - External Dependencies: Minimal - standard Python libraries only

**Object-Oriented Design Requirements**

1. Abstract Base Classes (ABC)
```
# Required abstract classes using abc module
- User (abstract base for Farmer and Buyer)
- Product (abstract base for different crop types)
- MarketPlace (abstract base for trading operations)
- USSDInterface (abstract base for menu systems)
```
2. Class Inheritance Hierarchy

```
# Inheritance structure requirements
User (ABC)
├── Farmer (inherits User)
└── Buyer (inherits User)

Product (ABC)
├── Crop (inherits Product)
├── Livestock (inherits Product)
└── ProcessedGood (inherits Product)

USSDInterface (ABC)
├── MainMenu (inherits USSDInterface)
├── FarmerMenu (inherits USSDInterface)
└── BuyerMenu (inherits USSDInterface)
```

**USSD Simulation Requirements**

- Menu Structure: Maximum 8 options per menu (USSD standard)
- Navigation: Support for *0 (back), *9 (main menu), #00 (exit)
- Session State: Maintain user context across menu levels
- Input Validation: Handle invalid inputs gracefully
- Response Format: Text-based responses under 160 characters per screen

**CLI Interface Specifications**

Console-based: Full terminal application simulation
Interactive Menus: Number-based option selection
Clear Feedback: Success/error messages for all operations
User-friendly: Simple language suitable for farmers
Responsive: Immediate feedback for all user actions

**Folder/File Structure**
```
AgroUSSD/
│
├── src/                          # Source code directory
│   ├── __init__.py
│   │
│   ├── models/                   # Data models and abstract classes
│   │   ├── __init__.py
│   │   ├── user.py              # Abstract User class
│   │   ├── farmer.py            # Farmer class (inherits User)
│   │   ├── buyer.py             # Buyer class (inherits User)
│   │   ├── product.py           # Abstract Product class
│   │   ├── crop.py              # Crop class (inherits Product)
│   │   └── harvest.py           # Harvest class
│   │
│   ├── services/                # Business logic and services
│   │   ├── __init__.py
│   │   ├── user_service.py      # User management operations
│   │   ├── market_service.py    # Market price operations
│   │   ├── harvest_service.py   # Harvest management
│   │   └── connection_service.py # Buyer-farmer connections
│   │
│   ├── interfaces/              # USSD interface classes
│   │   ├── __init__.py
│   │   ├── base_interface.py    # Abstract USSDInterface class
│   │   ├── main_menu.py         # Main menu interface
│   │   ├── farmer_menu.py       # Farmer-specific menus
│   │   ├── buyer_menu.py        # Buyer-specific menus
│   │   └── session_manager.py   # Session state management
│   │
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── data_handler.py      # File I/O operations
│   │   ├── validators.py        # Input validation
│   │   └── helpers.py           # Common helper functions
│   │
│   └── main.py                  # Main application entry point
│
├── data/                        # Data storage directory
│   ├── users.json              # User profiles storage
│   ├── harvests.json           # Harvest records storage
│   ├── market_prices.json      # Market price data
│   └── connections.json        # Buyer-farmer connections
│
├── tests/                      # Testing suite
│   ├── __init__.py
│   ├── test_models.py          # Model class tests
│   ├── test_services.py        # Service class tests
│   ├── test_interfaces.py      # Interface tests
│   └── test_integration.py     # End-to-end tests
│
├── docs/                       # Documentation
│   ├── architecture.md         # System architecture
│   ├── user_manual.md         # User guide
│   ├── api_reference.md       # Technical reference
│   └── class_diagrams/        # UML diagrams
│
├── demo/                       # Demonstration materials
│   ├── sample_data.json       # Test data sets
│   ├── user_scenarios.md      # Demo scenarios
│   └── presentation.pptx      # Project presentation
│
├── requirements.txt            # Python dependencies
├── README.md                  # Project overview
├── setup.py                   # Installation script
└── run.py                     # Application launcher

```

