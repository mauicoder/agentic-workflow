"""Multi-model Agentic TDD SDLC workflow script for Antigravity (agy).

Phase model assignments:
1. Initial architecture, spec-generation, and final orchestrator/merge phases:
   "Gemini 4 Argon"
2. Parallel ticket implementation and coding agents:
   "Gemini 4 Hydrogen"
"""

DEFAULT_ARCHITECT_MODEL = "Gemini 4 Argon"
DEFAULT_SPEC_MODEL = "Gemini 4 Argon"
DEFAULT_ORCHESTRATOR_MODEL = "Gemini 4 Argon"
DEFAULT_CODING_MODEL = "Gemini 4 Hydrogen"

workflow_args = globals().get("args") or {}

feature_slug = workflow_args.get("feature_slug", "feature")
requirements = workflow_args.get("requirements", "")
base_branch = workflow_args.get("base_branch", "main")
workspace_mode = workflow_args.get("workspace_mode", "share")
max_parallel = int(workflow_args.get("max_parallel", 3))

architecture_model = workflow_args.get(
    "architecture_model", DEFAULT_ARCHITECT_MODEL
)
spec_model = workflow_args.get("spec_model", DEFAULT_SPEC_MODEL)
coding_model = workflow_args.get(
    "coding_model",
    workflow_args.get("implementation_model", DEFAULT_CODING_MODEL),
)
orchestrator_model = workflow_args.get(
    "orchestrator_model",
    workflow_args.get("merge_model", DEFAULT_ORCHESTRATOR_MODEL),
)


def instantiate_agent(
    prompt,
    schema,
    role,
    model,
    type_name="self",
    workspace="inherit",
):
    """Instantiate a workflow agent with an explicit model parameter."""
    return agent(
        prompt=prompt,
        schema=schema,
        role=role,
        type_name=type_name,
        workspace=workspace,
        model=model,
    )


async def run_architecture_phase(slug, user_requirements, model=DEFAULT_ARCHITECT_MODEL):
    """Phase 1: Architecture alignment and requirement refinement using Gemini 4 Argon."""
    phase("Phase 1: Architecture & Requirement Refinement")
    log(f"Running architecture phase for '{slug}' with model='{model}'")
    arch_agent = instantiate_agent(
        prompt=(
            f"Analyze the codebase architecture and refine requirements for feature '{slug}'.\n"
            f"Requirements context: {user_requirements}\n"
            "Identify domain boundaries, shared interface contracts, and primary testing seams."
        ),
        schema={
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "testing_seams": {"type": "array", "items": {"type": "string"}},
                "contracts": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["summary", "testing_seams", "contracts"],
        },
        role=f"Architecture Refinement ({slug})",
        type_name="self",
        workspace="inherit",
        model=model,
    )
    return await arch_agent


async def run_spec_and_tickets_phase(
    slug, arch_context, model=DEFAULT_SPEC_MODEL
):
    """Phase 2 & 3: Specification synthesis and vertical-slice ticket DAG generation using Gemini 4 Argon."""
    phase("Phase 2 & 3: Specification & Ticket DAG Generation")
    log(f"Running spec and ticket generation for '{slug}' with model='{model}'")
    spec_agent = instantiate_agent(
        prompt=(
            f"Follow skills/to-spec/SKILL.md and skills/to-tickets/SKILL.md for feature '{slug}'.\n"
            f"Architecture context: {arch_context}\n"
            f"1. Write the formal specification to docs/specs/{slug}.md.\n"
            f"2. Slice the spec into dependency-graphed tracer-bullet tickets under docs/tickets/{slug}/.\n"
            "Return the spec path and ordered dependency waves of ticket paths."
        ),
        schema={
            "type": "object",
            "properties": {
                "spec_path": {"type": "string"},
                "waves": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
            "required": ["spec_path", "waves"],
        },
        role=f"Spec & Ticket Generator ({slug})",
        type_name="self",
        workspace="inherit",
        model=model,
    )
    return await spec_agent


def create_ticket_coding_agent(
    slug,
    spec_path,
    ticket_path,
    workspace="share",
    model=DEFAULT_CODING_MODEL,
):
    """Instantiate a parallel TDD coding agent for a single ticket using Gemini 4 Hydrogen."""
    return instantiate_agent(
        prompt=(
            f"Implement ticket '{ticket_path}' for spec '{spec_path}'.\n"
            "Read and strictly follow skills/tdd/SKILL.md (Red -> Green -> Refactor).\n"
            f"Work on a dedicated ticket branch off feat/{slug}, commit all passing tests and code, "
            "and return your branch name, ticket path, and test verification summary."
        ),
        schema={
            "type": "object",
            "properties": {
                "ticket": {"type": "string"},
                "branch": {"type": "string"},
                "tests_passed": {"type": "boolean"},
                "summary": {"type": "string"},
            },
            "required": ["ticket", "branch", "tests_passed", "summary"],
        },
        role=f"TDD Coding Agent ({ticket_path})",
        type_name="self",
        workspace=workspace,
        model=model,
    )


async def run_parallel_ticket_implementation(
    slug,
    spec_path,
    waves,
    workspace="share",
    batch_size=3,
    coding_agent_model=DEFAULT_CODING_MODEL,
    merge_agent_model=DEFAULT_ORCHESTRATOR_MODEL,
):
    """Phase 4: Execute unblocked ticket waves in parallel using Gemini 4 Hydrogen,
    merging completed batches onto the integration branch using Gemini 4 Argon.
    """
    phase("Phase 4: Parallel TDD Ticket Implementation")
    all_results = []

    for wave_index, wave_tickets in enumerate(waves, start=1):
        for i in range(0, len(wave_tickets), batch_size):
            batch = wave_tickets[i : i + batch_size]
            log(
                f"Wave {wave_index}: dispatching {len(batch)} parallel coding agent(s) "
                f"with model='{coding_agent_model}'"
            )
            batch_results = await parallel(
                batch,
                lambda ticket_path: create_ticket_coding_agent(
                    slug=slug,
                    spec_path=spec_path,
                    ticket_path=ticket_path,
                    workspace=workspace,
                    model=coding_agent_model,
                ),
            )
            all_results.extend(batch_results)

            log(
                f"Wave {wave_index}: merging completed ticket branches with "
                f"orchestrator model='{merge_agent_model}'"
            )
            wave_merge_agent = instantiate_agent(
                prompt=(
                    f"Merge the completed ticket branches for Wave {wave_index} into integration branch 'feat/{slug}':\n"
                    f"Completed tickets: {batch_results}\n"
                    "Verify the integration test suite passes cleanly and mark each merged ticket as 'done'."
                ),
                schema={
                    "type": "object",
                    "properties": {
                        "merged_branches": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "integration_tests_passed": {"type": "boolean"},
                    },
                    "required": ["merged_branches", "integration_tests_passed"],
                },
                role=f"Wave {wave_index} Orchestrator Merge ({slug})",
                type_name="self",
                workspace="inherit",
                model=merge_agent_model,
            )
            await wave_merge_agent

    return all_results


async def run_final_orchestrator_and_merge_phase(
    slug,
    spec_path,
    implemented_tickets,
    target_base_branch="main",
    model=DEFAULT_ORCHESTRATOR_MODEL,
):
    """Phase 5: Final orchestrator merge, two-axis verification, and branch finalization using Gemini 4 Argon."""
    phase("Phase 5: Final Orchestrator Merge & Two-Axis Review")
    log(f"Running final orchestrator/merge phase for '{slug}' with model='{model}'")

    review_axes = ["Standards", "Spec"]
    review_reports = await parallel(
        review_axes,
        lambda axis: instantiate_agent(
            prompt=(
                f"Follow skills/code-review/SKILL.md for the {axis} axis.\n"
                f"Compare integration branch 'feat/{slug}' against '{target_base_branch}' "
                f"using spec '{spec_path}'. Keep the report under 400 words."
            ),
            schema={"type": "string"},
            role=f"Code Review - {axis} Axis",
            type_name="research",
            workspace="inherit",
            model=model,
        ),
    )

    final_orchestrator = instantiate_agent(
        prompt=(
            f"Finalize integration branch 'feat/{slug}' against '{target_base_branch}'.\n"
            f"Spec: {spec_path}\n"
            f"Implemented tickets: {implemented_tickets}\n"
            f"Standards review report:\n{review_reports[0]}\n\n"
            f"Spec review report:\n{review_reports[1]}\n\n"
            "Ensure all ticket branches are cleanly merged, full test suites pass, "
            "and produce the final orchestrator summary."
        ),
        schema={
            "type": "object",
            "properties": {
                "integration_branch": {"type": "string"},
                "all_tests_passed": {"type": "boolean"},
                "standards_review": {"type": "string"},
                "spec_review": {"type": "string"},
                "summary": {"type": "string"},
            },
            "required": [
                "integration_branch",
                "all_tests_passed",
                "standards_review",
                "spec_review",
                "summary",
            ],
        },
        role=f"Final Orchestrator & Merge ({slug})",
        type_name="self",
        workspace="inherit",
        model=model,
    )
    return await final_orchestrator


arch_result = await run_architecture_phase(
    slug=feature_slug,
    user_requirements=requirements,
    model=architecture_model,
)

spec_and_tickets = await run_spec_and_tickets_phase(
    slug=feature_slug,
    arch_context=arch_result,
    model=spec_model,
)

ticket_results = await run_parallel_ticket_implementation(
    slug=feature_slug,
    spec_path=spec_and_tickets["spec_path"],
    waves=spec_and_tickets["waves"],
    workspace=workspace_mode,
    batch_size=max_parallel,
    coding_agent_model=coding_model,
    merge_agent_model=orchestrator_model,
)

final_summary = await run_final_orchestrator_and_merge_phase(
    slug=feature_slug,
    spec_path=spec_and_tickets["spec_path"],
    implemented_tickets=ticket_results,
    target_base_branch=base_branch,
    model=orchestrator_model,
)

log(f"Workflow complete for '{feature_slug}': {final_summary['summary']}")
final_summary
