import argparse as ap
import os
import glob
import pickle
import sys
import csv
import database_filtering
from database_filtering.utils.utils import filter_mols
from database_filtering.utils.utils import generate_alternative_scaffolds
import rdkit
from rdkit import Chem


def parse_args(args):
    parser = ap.ArgumentParser()
    parser.add_argument("-i","--template_ligand", type=str, required=True,
                        help="Path to PDB template ligand.")
    parser.add_argument("-l","--ligands", type=str, required=True,
                        help="Path to SDF file with ligands.")
    parser.add_argument("-o", "--outfile", required=True, help="Output file name.")
    parser.add_argument("-a", "--atom_linker", required = True, nargs='+', help = " Carbon atom of core that is bound to r-group.")
    parser.add_argument("-s", "--scaffold_alternatives", required=False, help="Alternative atom types in scaffold.")
    parsed_args = parser.parse_args(args)
    return parsed_args


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    linkers = [args.atom_linker]
    if args.scaffold_alternatives:
        template_ligs, linkers = generate_alternative_scaffolds(args.template_ligand, args.scaffold_alternatives, linkers[0])
    else:
        template_ligs = [Chem.MolFromSmiles(args.template_ligand.replace("'",""))]
    ligands_path = args.ligands
    outfile= args.outfile
    dirs = glob.glob(ligands_path + "/*.sd*")
    ligands=[]
    i=0
    while i < len(dirs):
        if os.path.isdir(dirs[i]):
            dirs = dirs + glob.glob(dirs[i] + "/*")
        else:
            if os.path.splitext(dirs[i])[1] == '.sd' or os.path.splitext(dirs[i])[1] == ".sdf":
                ligands.append(dirs[i])
        i+=1

    for template_lig,linker in zip(template_ligs, linkers):
        import rdkit
        from rdkit import Chem
        Chem.MolToPDBFile(template_lig,f"res_{os.path.splitext(os.path.basename(args.template_ligand))[0]}.pdb")
        filter_mols(template_lig,ligands,f"{os.path.splitext(os.path.basename(args.template_ligand))[0]}_{outfile}_{i}",linker)
