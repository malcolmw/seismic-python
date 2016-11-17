#! /usr/bin/env python
from seispy.locate import Locator
from seispy.util import MultiThreadProcess
from gazelle.datascope import Database
import argparse
import ConfigParser


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("db", type=str, nargs=1)
    parser.add_argument("config", type=str, nargs=1)
    return parser.parse_args()


def parse_config(args):
    cfg = {}
    config = ConfigParser.RawConfigParser()
    config.read(args.config[0])
    cfg["tt_dir"] = config.get("General", "tt_dir")
    cfg["mode"] = config.get("General", "mode")
    cfg["author"] = config.get("General", "author")
    cfg["n_threads"] = config.getint("General", "n_threads")
    cfg["min_nsta"] = config.getint("General", "min_nsta")
    cfg["P_residual_tolerance"] = config.getfloat("General",
                                                  "P_residual_tolerance")
    cfg["S_residual_tolerance"] = config.getfloat("General",
                                                  "S_residual_tolerance")
    cfg["convergance_threshold"] = config.getfloat("General",
                                                   "convergance_threshold")
    cfg["max_iterations"] = config.getint("General", "max_iterations")
    cfg["input_q_size"] = config.getint("General", "input_q_size")
    cfg["output_q_size"] = config.getint("General", "output_q_size")
    return cfg


def getter(db):
    print "INITIALIZE REAP THREAD"
    for origin in db.iterate_events(parse_magnitudes=False):
        yield origin


def main_processor(origin, db, cfg):
    locator = Locator(cfg)
    if cfg['mode'] == 'relocate':
        return locator.relocate(origin)
    elif cfg['mode'] == 'locate':
        return locator.locate(origin)
    else:
        print "invalid mode: %s" % cfg['mode']
        exit()


def outputter(origin, db, cfg):
    if origin is None:
        return
    if cfg['mode'] == 'relocate':
        auth = cfg['author'] + ":reloc"
    elif cfg['mode'] == 'locate':
        auth = cfg['author'] + ":loc"
    origin.author = auth
    print origin.check_network_geometry(), origin.check_azimuthal_gap(), origin
    origin.plot_special()
    # db.write_origin(origin)


def main():
    db = Database(args.db[0], mode='r+')
    config_params = {'n_threads': cfg['n_threads'],
                     'input_q_max_size': cfg['input_q_size'],
                     'output_q_max_size': cfg['output_q_size']}
    extra_args = {'input_init_args': (db,),
                  'main_init_args': (db, cfg),
                  'output_init_args': (db, cfg)}
    mtp = MultiThreadProcess(getter,
                             main_processor,
                             outputter,
                             extra_args=extra_args,
                             config_params=config_params)
    mtp.start()
    db.close()

if __name__ == "__main__":
    args = parse_args()
    cfg = parse_config(args)
    main()
