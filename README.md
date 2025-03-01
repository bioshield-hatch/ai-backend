# ai-backend
The eventual goal is to train an AI on data of what viruses and pathogens look like on microscope slides to then point them out on various images


## Pocketbase Config/Setup
1. Download the pocketbase .zip from https://pocketbase.io
2. Rename the extracted folder to `pb` and move to the project root directory
3. Open a terminal, navigate into the `pb` folder, and run `pocketbase serve`
4. Click the admin UI link or navigate to http://127.0.0.1:8090/_/ in a web browser and follow the instructions to create an account.
5. Once in the admin UI, go to settings (3rd icon on left navbar) -> Import Collections and paste in the content of `pocketbase-config.json` into the import field.
6. After finishing the import, create a standard user by going to the Collections tab (1st icon on left navbar) -> Users -> New Record and fill the information.