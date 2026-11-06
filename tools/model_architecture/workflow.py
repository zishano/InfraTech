"""Create a reusable, explicitly unreviewed model architecture study workspace."""
import copy
import json
from pathlib import Path

CHECKS={
    'identity_and_sources':'Target/baseline identity, pinned revisions, source IDs, hashes, observed failures.',
    'checkpoint_parameters':'Actual checkpoint values; text/vision scopes; class defaults and rounding kept separate.',
    'layer_schedule':'Exact main/auxiliary counts and 0-based versus 1-based numbering.',
    'attention_and_gates':'Q/K/V, recurrent controls, output gates, normalization and positional operations.',
    'cache_and_visibility':'KV/index/state buffers, prefill/decode writes, causal masks, top-k reads versus storage.',
    'moe_residual_vision_auxiliary':'Routed/shared experts, latent paths, weight placement, residuals, vision, MTP.',
    'version_diff':'Source-reviewed structural additions/removals versus parameter/config-only changes.',
    'software_hardware_scope':'Introduced/inherited/backend-specific optimizations; weight/activation/cache precision.',
    'visual_expression':'Short operator labels, readable type hierarchy, adjacent panels, tensor-state insets.',
    'routing_and_layout':'Aligned straight edges first; required branches preserved; actual renderer checks.',
    'native_delivery':'Direct draw.io→PNG export, paired manifests and detailed-page consistency.',
    'validation_and_sync':'Relevant checks, honest limitations, user-authorized branch commit/push.'
}

def create_study(manifest,out,baseline=None):
    """Scaffold review records, never approve facts or overwrite existing work."""
    out=Path(out)
    model=manifest['model']
    review=dict(version=1,model=model,requested_revision=manifest.get('revision'),
      status='pending',workflow='tools/model_architecture/WORKFLOW.md',
      baseline=None if baseline is None else dict(model=baseline['model'],requested_revision=baseline.get('revision')),
      source_policy=dict(pin_revisions=True,unique_source_ids=True,execute_remote_code=False,download_full_weights=False),
      architecture=dict(main_layers=None,auxiliary_layers=None,layer_numbering=None,attention_paths=[],cache_contracts=[],unresolved=[]),
      version_diff=dict(themes=dict(added='red',removed='green',parameter_changed='yellow',unchanged='neutral'),
                        additions=[],removals=[],parameter_changes=[],baseline_clarifications=[]),
      optimization_claims=[],
      claim_fields=['claim','classification: introduced/inherited/backend_specific/unverified','source_id','locator','applicable_backend_or_hardware','measurement_scope'],
      presentation=dict(flow='bottom-up',labels='operator + necessary dimensions; typically 1–2 lines',
                        node_sizing='operator visual complexity + name/dimensions + branch interfaces; preserve lane centers',
                        routing_priority=['straight_if_clear','one_bend_if_clear','necessary_detour'],
                        long_notes='description / evidence / README',native_png_source='drawio'),
      checks={key:dict(status='pending',question=value,evidence=[],notes='') for key,value in CHECKS.items()},
      delivery=dict(graph=None,drawio=None,png=None,export_manifest=None,layout_report=None,authorized_branch=None),
      limitations=['Scaffold only: no sources collected, topology reviewed, renderer run or model inference executed.'])
    lines=['# '+model+' 架构审阅记录','',
           '先阅读仓库工具目录的 `WORKFLOW.md`。此文件是待填写模板，不表示资料已收集或结构已核实。','',
           '## 模型和来源','',
           '- 目标模型／变体：'+model,
           '- 已核对固定 revision：待填写（请求值：'+str(manifest.get('revision'))+'）',
           '- 基线模型／固定 revision：'+('无' if baseline is None else baseline['model']+' / '+str(baseline.get('revision'))),
           '- 来源获取、哈希、失败／未公开内容：待填写','',
           '## 结构审阅','']
    for key,text in CHECKS.items():lines.append('- [ ] `'+key+'`：'+text)
    lines.extend(['','## 主要计算与状态','',
       '| 模块 | 输入／分支 | 算子顺序 | 状态写入／读取 | 来源及定位 | 未确认项 |',
       '| --- | --- | --- | --- | --- | --- |',
       '| 待审阅 | | | | | |','',
       '## 模型版本差异','',
       '| 旧内容 | 新内容 | 红新增／绿退役／黄参数／中性澄清 | 来源 | 是否接入当前推理 |',
       '| --- | --- | --- | --- | --- |','| 待审阅 | | | | |','',
       '## 训练与软硬协同声明','',
       '| 声明 | 新增／沿用／后端实现／待核实 | 来源 | 适用硬件和后端 | 实测或资料声明 |',
       '| --- | --- | --- | --- | --- |','| 待审阅 | | | | |','',
       '## 交付','',
       '- 原生 draw.io、直接导出的 PNG、layout / export 记录：待生成。',
       '- GPU推理、数值等价、完整权重形状与飞书导入：未执行，不得声称通过。',
       '- 用户已授权的提交分支：待按会话填写。',''])
    files={
      'sources.json':json.dumps(copy.deepcopy(manifest),ensure_ascii=False,indent=2)+'\n',
      'review.json':json.dumps(review,ensure_ascii=False,indent=2)+'\n',
      'architecture_review.md':'\n'.join(lines),
    }
    if baseline is not None:files['baseline.sources.json']=json.dumps(copy.deepcopy(baseline),ensure_ascii=False,indent=2)+'\n'
    # Validate all output destinations before creating anything.
    for name in files:
        dest=out/name
        if dest.exists() or dest.is_symlink():raise FileExistsError('Refusing to overwrite study file: '+str(dest))
    out.mkdir(parents=True,exist_ok=True)
    for name,content in files.items():
        with (out/name).open('x',encoding='utf-8') as f:f.write(content)
    return [str(out/name) for name in files]
