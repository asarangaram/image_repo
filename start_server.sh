#! /bin/bash

set -e

create_venv() {
    V_ENV=".venv"
    
    if [ ! -d "$V_ENV" ]; then
        echo "$V_ENV does not exist. Creating"
        python3 -m venv .venv
        if [ -f "${V_ENV}/bin/activate" ]; then
            source "${V_ENV}/bin/activate"
        else
            echo "Error: Virtual environment activation script not found."
            exit 1
        fi
        # Example: Call the function with a specific requirements file
        install_packages_from_requirements "requirements.txt"
    else
        echo "$V_ENV Found"
        if [ -f "${V_ENV}/bin/activate" ]; then
            source "${V_ENV}/bin/activate"
        else
            echo "Error: Virtual environment activation script not found."
            exit 1
        fi
    fi
    
}

install_packages_from_requirements() {
    requirements_file="$1"
    echo "install pacakges if missing"
    if [ -f "$requirements_file" ]; then
        while IFS= read -r requirement; do
            package_name=$(echo "$requirement" | cut -d'=' -f1)
            if ! pip show "$package_name" > /dev/null 2>&1; then
                
                echo "Installing $requirement..."
                pip install "$requirement"
            fi
        done < "$requirements_file"
    else
        echo "Error: $requirements_file not found."
        exit 1
    fi
}

# Call the function
create_venv

avahi-publish-service -s "CL IMAGE REPO" _image_repo_api._tcp 5000 "CL Image Repo Service" &
python -m src.wsgi

