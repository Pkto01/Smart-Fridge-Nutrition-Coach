{
  description = "python smart fridge";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [ 
          postgresql
          libpq
          python314Packages.psycopg2-binary
        ];
        packages = with pkgs;[
          python314
          direnv
          nix-direnv
          dbeaver-bin
        ];
        shellHook = ''
         export PS1="(dev shell python) \[\e[38;5;75m\]\u@\h \[\e[38;5;113m\]\w \[\e[38;5;189m\]\$ \[\e[0m\]"
         echo "Setting up PostgreSQL..."
         export PGDATA="$PWD/.pg_data"
         export PGHOST="$PWD/.pg_socket"
         export PGDATABASE="mydb"
         mkdir -p "$PGHOST"
         if [ ! -d "$PGDATA" ]; then
           initdb --auth=trust --no-locale -D "$PGDATA"
         fi
         pg_ctl -D "$PGDATA" -o "--unix_socket_directories='$PGHOST'" -l "$PGDATA/log" start

         # DB creation si pas encore créer
         if ! psql -lqt | cut -d '|' -f 1 | grep -qw "$PGDATABASE"; then
           createdb "$PGDATABASE"
         fi

         trap "pg_ctl -D \"$PGDATA\" stop" EXIT
         
         echo "setting up python env..."
         python3 -m venv venv
         source ./venv/bin/activate

         # Project related
         export DB_URL="postgresql://localhost:5432/$PGDATABASE"
         export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.postgresql.lib ]}:$LD_LIBRARY_PATH"

         
         pip install fastapi pydantic pydantic-settings fastapi[standard] fastapi-cache2 requests psycopg psycopg_pool
         
         2>/dev/null 1>/dev/null dbeaver &
         
         fastapi dev main.py
        '';
      };
    };
}