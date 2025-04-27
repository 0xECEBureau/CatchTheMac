# Use an official PHP image with Apache
FROM php:8.2-apache

# Set secure configurations
RUN a2enmod rewrite \
    && docker-php-ext-install mysqli pdo pdo_mysql \
    && echo "ServerTokens Prod\nServerSignature Off" >> /etc/apache2/conf-available/security.conf \
    && a2enconf security

# Set permissions (avoid running as root)
RUN useradd -m ctfuser && chown -R ctfuser:www-data /var/www/html

# Copy the PHP application files
COPY . /var/www/html

# Change working directory
WORKDIR /var/www/html

# Expose port 80
EXPOSE 80

# Use non-root user
USER ctfuser

CMD ["apache2-foreground"]
