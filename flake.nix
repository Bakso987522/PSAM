{
  description = "Agrolupa dev";

  inputs = {
    nixpkgs.url = "https://channels.nixos.org/nixpkgs-unstable/nixexprs.tar.zst";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAllSystems (pkgs:
        let
          aliases = {
            lg = "lazygit";
          };
          aliasPkgs = pkgs.lib.mapAttrsToList
            (name: cmd: pkgs.writeShellScriptBin name "${cmd} \"$@\"")
            aliases;
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              python3
              nodejs_26
              pnpm
              go-task
              lazygit
            ] ++ aliasPkgs;

            shellHook = ''
              echo "===================="
              echo "ITS CODING TIME"
              echo "===================="
            '';
          };
        });
    };
}
