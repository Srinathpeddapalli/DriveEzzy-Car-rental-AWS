# Drive Ezzy: Scalable Car Rental Platform

## Project Description
The Drive Ezzy project is a cloud-based, scalable car rental platform designed to streamline the vehicle rental process for users looking to rent sedans, SUVs, and mini camper vans. Developed using Flask for backend management and hosted on AWS EC2 with Amazon RDS for database support, the platform ensures secure, efficient, and reliable user interactions. Drive Ezzy simplifies car rental by enabling users to browse available vehicles, choose rental periods, add special requests, and manage payments, delivering a smooth and scalable customer experience.

## Key Scenarios

### Scenario 1: Scalable Infrastructure for Car Rental Bookings
During peak travel times, Drive Ezzy needs to handle high volumes of traffic as customers book rentals. AWS EC2 provides an auto-scaling solution that keeps the platform responsive and fast, even under heavy user loads. Flask powers the backend, managing essential functionalities like user sessions, car availability, booking details, and payments. This setup allows Drive Ezzy to support increased demand without performance issues.

### Scenario 2: Efficient Database Management for Car Reservations
Efficiently managing booking data, customer profiles, vehicle availability, and payment records is critical for a car rental platform. Drive Ezzy utilizes Amazon RDS with a managed MySQL database for automated backups, high availability, and reliable performance. The RDS database seamlessly manages customer information, rental histories, and vehicle availability updates, ensuring data consistency and scalability as the platform grows.

### Scenario 3: Secure and Reliable Hosting for Car Rental Services
For security and reliability, AWS EC2 hosts the Drive Ezzy platform, which handles customer bookings, vehicle inventory, and special requests. Integrated with AWS IAM (Identity and Access Management), the platform enforces strict access control, ensuring that only authorized users can access sensitive information and administrative functions. EC2’s flexible resource allocation allows the platform to adjust to traffic fluctuations, maintaining a stable and secure experience for all users.

## Technologies Used
- **Backend**: Flask
- **Cloud Hosting**: AWS EC2
- **Database Management**: Amazon RDS (MySQL)
- **Access Management**: AWS IAM

## Usage
1. Clone the repository to your local environment.
2. Follow the setup instructions in the documentation to deploy the platform on AWS EC2 and connect to Amazon RDS.
3. Start the Flask application and explore features such as vehicle browsing, booking, and payment processing.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to AWS for providing the cloud infrastructure solutions.
- Special thanks to the Flask and Python communities for resources and support in backend development.

![Drive Ezzy Platform Screenshot](https://your-image-link-here.com)  <!-- Replace with an actual image link if available -->

