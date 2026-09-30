import os
import glob
import ROOT
from ROOT import RDataFrame


ROOT.EnableImplicitMT()


def rename(inputfile, outputfile):
    os.makedirs(os.path.dirname(outputfile), exist_ok=True)

    df = RDataFrame("tree", inputfile)

    df = df.Define(
        "label_QCD", "1 - is_signal").Define(
        "label_Tbqq", "(gen_match==11) + (gen_match==12)").Define(
        "label_Tbl", "(gen_match==15) + (gen_match==16)").Define(
        "label_Wqq", "(gen_match==21) + (gen_match==22)").Define(
        "label_Zqq", "(gen_match==31) + (gen_match==32) + (gen_match==33)").Define(
        "label_Hbb", "gen_match==41").Define(
        "label_Hcc", "gen_match==42").Define(
        "label_Hgg", "gen_match==44").Define(
        "label_H4q", "gen_match==45").Define(
        "label_Hqql", "gen_match==46")

    df = df.Define(
        "PID", "abs(part_pid)").Define(
        "part_isChargedHadron", "(PID==211) + (PID==321) + (PID==2212)").Define(
        "part_isNeutralHadron", "PID==0").Define(
        "part_isPhoton", "PID==22").Define(
        "part_isElectron", "PID==11").Define(
        "part_isMuon", "PID==13")

    df = df.Alias(
        "aux_truth_match", "gen_match").Alias(
        "aux_genpart_pt", "genpart_pt").Alias(
        "aux_genpart_eta", "genpart_eta").Alias(
        "aux_genpart_phi", "genpart_phi").Alias(
        "aux_genpart_pid", "genpart_pid")

    # branches = [str(n) for n in df.GetColumnNames()]
    # keep_branches = [n for n in branches if n not in ('part_pt', 'part_pid') and (
    #     n.startswith('label_') or n.startswith('aux_') or n.startswith('jet_') or n.startswith('part_'))]

    keep_branches = [  # noqa
        'part_px', 'part_py', 'part_pz', 'part_energy',
        'part_deta', 'part_dphi',
        'part_d0val', 'part_d0err', 'part_dzval', 'part_dzerr',
        'part_charge', 'part_isChargedHadron', 'part_isNeutralHadron', 'part_isPhoton', 'part_isElectron', 'part_isMuon',

        'label_QCD',
        'label_Hbb', 'label_Hcc', 'label_Hgg', 'label_H4q', 'label_Hqql',
        'label_Zqq', 'label_Wqq', 'label_Tbqq', 'label_Tbl',

        'jet_pt', 'jet_eta', 'jet_phi', 'jet_energy', 'jet_nparticles', 'jet_sdmass', 'jet_tau1', 'jet_tau2', 'jet_tau3', 'jet_tau4',

        'aux_genpart_eta', 'aux_genpart_phi', 'aux_genpart_pid', 'aux_genpart_pt', 'aux_truth_match',

        'genjet_matched', 'genjet_dr', 'genjet_pt', 'genjet_eta', 'genjet_phi', 'genjet_energy', 'genjet_nparticles',
        'genjet_sdmass', 'genjet_tau1', 'genjet_tau2', 'genjet_tau3', 'genjet_tau4',

        'genjet_part_px', 'genjet_part_py', 'genjet_part_pz', 'genjet_part_energy', 'genjet_part_pt',
        'genjet_part_deta', 'genjet_part_dphi', 'genjet_part_charge', 'genjet_part_pid', 'genjet_part_histidx',

        'genjet_nhist', 'genjet_hist_pt', 'genjet_hist_eta', 'genjet_hist_phi', 'genjet_hist_mass', 'genjet_hist_energy',
        'genjet_hist_pid', 'genjet_hist_status', 'genjet_hist_charge', 'genjet_hist_index',
        'genjet_hist_statusflags', 'genjet_hist_levelflags', 'genjet_hist_vtx', 'genjet_hist_vtxreason',
        'genjet_hist_edge_mother', 'genjet_hist_edge_daughter',
    ]

    opt = ROOT.RDF.RSnapshotOptions()
    opt.fCompressionAlgorithm = ROOT.kLZ4
    opt.fCompressionLevel = 4

    df.Snapshot("tree", outputfile, ROOT.std.vector(ROOT.std.string)(keep_branches), opt)


basedir = 'dataset/JetClass/'
subdirs = ('val_5M', 'test_20M', 'train_100M')
# subdirs = ('train_1M',)
for subdir in subdirs:
    fpaths = os.path.join(basedir, subdir, '*.root')
    print(fpaths)
    files = glob.glob(fpaths)
    for inputfile in files:
        outputfile = inputfile.replace('JetClass', 'JetClass-renamed')
        rename(inputfile, outputfile)
        print(outputfile)
