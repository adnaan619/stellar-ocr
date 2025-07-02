FROM jenkins/jenkins:2.414.1-lts-jdk11

# Switch to root to install Docker
USER root

# Install Docker CLI and Docker Compose
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Create docker group and add jenkins user to it
RUN groupadd -f docker && usermod -aG docker jenkins

# Install additional tools
RUN apt-get install -y \
    git \
    nodejs \
    npm \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create directories and switch back to jenkins user
USER jenkins
RUN mkdir -p /var/jenkins_home/casc_configs

# Copy Jenkins configuration
COPY jenkins.yaml /var/jenkins_home/casc_configs/jenkins.yaml

# Set environment variables
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc_configs
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"
