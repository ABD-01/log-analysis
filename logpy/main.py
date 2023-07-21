import warnings
from .utils import Parser
from .logutils import MODULE_SUBFUNCTIONS, MODULE_ADDLOG
from .logutils import LogAnalyzer, BasicLog


def main():
    parser = Parser(**MODULE_SUBFUNCTIONS)
    p = parser.parse_args()

    log_analyzer = LogAnalyzer(p)

    if p.module is None:
        p.all = True

    if p.all:
        for add_logs in MODULE_ADDLOG.values():
            for f in add_logs.values():
                f(log_analyzer, p)

    else:
        for module, subfuncs in MODULE_SUBFUNCTIONS.items():
            if p.module == module:
                all_funt = True
                for subfunc in subfuncs:
                    if getattr(p, subfunc):
                        MODULE_ADDLOG[module][subfunc](log_analyzer, p)
                        all_funt = False
                if all_funt:
                    for f in MODULE_ADDLOG[module].values():
                        f(log_analyzer, p)


    for kw in p.keywords:
        log_analyzer.add_log_type(BasicLog(kw, kw, ignore_case=p.ignore_case))
    
    if p.regex:
        warning_msg = "Warning: --regex argument is not implemented yet. It will be added in a future update."
        warnings.warn(warning_msg, category=FutureWarning)

    log_analyzer.analyze()
    log_analyzer.print_summary(p.show_empty)


if __name__ == "__main__":
    parser = Parser(**MODULE_SUBFUNCTIONS)
    args = parser.parse_args()
    main()
