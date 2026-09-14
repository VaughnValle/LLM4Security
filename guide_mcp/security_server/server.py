from pathlib import Path


def load_trusthub_case(case_name: str, guide_root: Path) -> dict:
    raise NotImplementedError("TODO: Trust-Hub metadata loader")


def evaluate_trojan_detection(reference: Path, candidate: Path) -> dict:
    raise NotImplementedError("TODO: controlled Trojan evaluation metrics")
